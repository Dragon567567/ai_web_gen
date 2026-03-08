import os
import json
import shutil
import subprocess
import time
import random
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.routers.auth import get_current_user

router = APIRouter()

# 部署目录
DEPLOY_BASE_DIR = "C:\\Users\\longz\\PycharmProjects\\ai_web_gen\\deployed_apps"


def get_app_port():
    """获取一个随机可用端口（8001-9000）"""
    return random.randint(8001, 9000)


def get_host_ip():
    """获取宿主机 IP"""
    try:
        result = subprocess.check_output('ipconfig', shell=True).decode()
        lines = result.split('\n')
        host_ip = '192.168.21.6'
        for line in lines:
            if 'IPv4' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    ip = parts[1].strip()
                    if ip and not ip.startswith('127'):
                        host_ip = ip
                        break
    except:
        host_ip = '192.168.21.6'
    return host_ip


def deploy_frontend_node(frontend_files, app_id, app_dir, backend_port, log):
    """部署前端 Node.js 项目（需要构建）"""
    # 写入所有文件
    for file_item in frontend_files:
        filepath = os.path.join(app_dir, file_item['filename'])
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(file_item['content'])

    # 检查是否有构建命令
    package_json = None
    for f in frontend_files:
        if f['filename'] == 'package.json':
            package_json = json.loads(f['content'])
            break

    build_cmd = package_json.get('scripts', {}).get('build', 'vite build') if package_json else 'vite build'
    dev_cmd = package_json.get('scripts', {}).get('dev', 'vite') if package_json else 'vite'

    log(f"检测到 Node.js 项目，将执行构建命令: {build_cmd}")

    # 创建 Dockerfile (Node.js + nginx)
    dockerfile_content = f"""FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run {build_cmd}

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf.d/*.conf /etc/nginx/conf.d/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
    with open(os.path.join(app_dir, "Dockerfile"), "w", encoding="utf-8") as fp:
        fp.write(dockerfile_content)

    # 创建 nginx 配置
    nginx_config = f"""server {{
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # API 代理
    location /api/ {{
        proxy_pass http://{get_host_ip()}:{backend_port}/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    location / {{
        try_files $uri $uri/ /index.html;
    }}

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {{
        root /usr/share/nginx/html;
    }}
}}
"""
    # 如果没有后端，移除 API 代理
    if not backend_port:
        nginx_config = """server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    location / {
        try_files $uri $uri/ /index.html;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
"""

    nginx_conf_dir = os.path.join(app_dir, "nginx.conf.d")
    os.makedirs(nginx_conf_dir, exist_ok=True)
    with open(os.path.join(nginx_conf_dir, "default.conf"), "w", encoding="utf-8") as fp:
        fp.write(nginx_config)

    # 获取端口
    port = get_app_port()
    image_name = f"ai_web_gen_frontend_{app_id}"

    # 构建 Docker 镜像
    log(f"正在构建前端 Docker 镜像 (端口: {port})...")
    try:
        build_cmd = f'docker build -t {image_name} "{app_dir}"'
        result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"构建失败 - {result.stderr}"
        log("前端 Docker 镜像构建成功")
    except Exception as e:
        return None, port, str(e)

    # 运行容器
    log("正在启动前端容器...")
    try:
        subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
        subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)

        run_cmd = f'docker run -d --name {image_name} -p {port}:80 {image_name}'
        result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"启动失败 - {result.stderr}"

        # 等待几秒后检查容器状态
        time.sleep(3)
        check_result = subprocess.run(
            f"docker inspect -f '{{{{.State.Running}}}}' {image_name}",
            shell=True, capture_output=True, text=True
        )
        if "true" not in check_result.stdout:
            # 获取容器日志
            try:
                logs_result = subprocess.run(
                    ["docker", "logs", "--tail", "50", image_name],
                    capture_output=True, text=True, timeout=10
                )
                container_logs = logs_result.stdout + logs_result.stderr if logs_result.stdout or logs_result.stderr else "无法获取日志"
            except Exception as e:
                container_logs = f"获取日志失败: {str(e)}"
            # 停止并删除容器
            subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
            subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)
            return None, port, f"容器启动后未运行. 错误日志: {container_logs[:500]}"

        log("前端容器启动成功")
    except Exception as e:
        return None, port, str(e)

    return f"http://{get_host_ip()}:{port}", port, None


def deploy_frontend(frontend_files, app_id, app_dir, backend_port, log):
    """部署前端"""
    # 检查是否有 package.json（Node.js 项目）
    has_package_json = any(f['filename'] == 'package.json' for f in frontend_files)

    # 如果有 package.json，需要构建 Node.js 项目
    if has_package_json:
        return deploy_frontend_node(frontend_files, app_id, app_dir, backend_port, log)

    # 否则按静态文件处理
    # 找到 index.html
    index_file = None
    other_files = []
    for file_item in frontend_files:
        if file_item['filename'] == 'index.html':
            index_file = file_item
        else:
            other_files.append(file_item)

    # 创建 index.html
    if index_file:
        index_content = index_file['content']
        # 如果有后端端口，注入到前端代码中
        if backend_port:
            # 创建一个配置脚本
            backend_full_url = f"http://192.168.21.6:{backend_port}"
            config_script = f"""
<script>
  window.API_BASE_URL = "{backend_full_url}";
</script>
"""
            # 在 </head> 之前插入配置
            if '</head>' in index_content:
                index_content = index_content.replace('</head>', config_script + '</head>')
            elif '<body' in index_content:
                index_content = index_content.replace('<body', config_script + '<body')

        with open(os.path.join(app_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(index_content)

    # 创建其他静态文件
    for file_item in other_files:
        filepath = os.path.join(app_dir, file_item['filename'])
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(file_item['content'])

    # 创建 nginx 配置（支持 SPA、CORS 和 API 代理）
    nginx_config = f"""server {{
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # API 代理 - 将 /api/ 请求转发到后端
    location /api/ {{
        proxy_pass http://{get_host_ip()}:{backend_port}/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    # 处理 CORS 预检请求
    location = / {{
        # CORS headers
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE" always;
        add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
        add_header Access-Control-Allow-Credentials "true" always;

        # 处理 OPTIONS 预检请求
        if ($request_method = 'OPTIONS') {{
            add_header Access-Control-Allow-Origin "*" always;
            add_header Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE" always;
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
            add_header Access-Control-Allow-Credentials "true" always;
            add_header Access-Control-Max-Age 1728000 always;
            return 204;
        }}

        # Vue history mode - SPA 支持
        try_files $uri $uri/ /index.html;
    }}

    # Error pages
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {{
        root /usr/share/nginx/html;
    }}
}}
"""
    # 创建 nginx 配置目录
    nginx_conf_dir = os.path.join(app_dir, "nginx.conf.d")
    os.makedirs(nginx_conf_dir, exist_ok=True)

    # 替换后端端口占位符
    if backend_port:
        # 使用 localhost 因为容器使用 --network host
        backend_url = f"192.168.21.6:{backend_port}"
        log(f"配置前端 nginx 代理到后端: {backend_url}")
        nginx_config = nginx_config.replace("BACKEND_PORT", backend_port)
    else:
        log("警告: 没有后端端口，前端将无法调用 API")
        # 如果没有后端，使用简化配置（无 API 代理）
        nginx_config = """server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    location / {
        try_files $uri $uri/ /index.html;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
"""

    with open(os.path.join(nginx_conf_dir, "default.conf"), "w", encoding="utf-8") as fp:
        fp.write(nginx_config)

    # 创建 Dockerfile (nginx)
    dockerfile_content = """FROM nginx:alpine
COPY nginx.conf.d/*.conf /etc/nginx/conf.d/
COPY . /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
    with open(os.path.join(app_dir, "Dockerfile"), "w", encoding="utf-8") as fp:
        fp.write(dockerfile_content)

    # 获取端口
    port = get_app_port()
    image_name = f"ai_web_gen_frontend_{app_id}"

    # 构建 Docker 镜像
    log(f"正在构建前端 Docker 镜像 (端口: {port})...")
    try:
        build_cmd = f'docker build -t {image_name} "{app_dir}"'
        result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"构建失败 - {result.stderr}"
        log("前端 Docker 镜像构建成功")
    except Exception as e:
        return None, port, str(e)

    # 运行容器
    log("正在启动前端容器...")
    try:
        # 先停止可能存在的同名容器
        subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
        subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)

        run_cmd = f'docker run -d --name {image_name} -p {port}:80 {image_name}'
        result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"启动失败 - {result.stderr}"

        # 等待几秒后检查容器状态
        time.sleep(3)
        check_result = subprocess.run(
            f"docker inspect -f '{{{{.State.Running}}}}' {image_name}",
            shell=True, capture_output=True, text=True
        )
        if "true" not in check_result.stdout:
            try:
                logs_result = subprocess.run(
                    ["docker", "logs", "--tail", "50", image_name],
                    capture_output=True, text=True, timeout=10
                )
                container_logs = logs_result.stdout + logs_result.stderr if logs_result.stdout or logs_result.stderr else "无法获取日志"
            except Exception as e:
                container_logs = f"获取日志失败: {str(e)}"
            subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
            subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)
            return None, port, f"容器启动后未运行. 错误日志: {container_logs[:500]}"

        log("前端容器启动成功")
    except Exception as e:
        return None, port, str(e)

    return f"http://{get_host_ip()}:{port}", port, None


def deploy_backend_go(backend_files, app_id, app_dir, log):
    """部署后端 Go 项目"""
    # 写入后端文件
    main_file = None
    for file_item in backend_files:
        filepath = os.path.join(app_dir, file_item['filename'])
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(file_item['content'])

        if file_item['filename'].endswith('.go'):
            main_file = file_item['filename']

    # 创建 Dockerfile
    dockerfile_content = f"""FROM golang:1.21-alpine as build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server {'-tags netgo' if main_file else ''} {main_file or 'main.go'}

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=build /app/server .
EXPOSE 8080
CMD ["./server"]
"""
    with open(os.path.join(app_dir, "Dockerfile"), "w", encoding="utf-8") as fp:
        fp.write(dockerfile_content)

    # 获取端口
    port = get_app_port()
    image_name = f"ai_web_gen_backend_{app_id}"

    # 构建 Docker 镜像
    log(f"正在构建后端 Go Docker 镜像 (端口: {port})...")
    try:
        build_cmd = f'docker build -t {image_name} "{app_dir}"'
        result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"构建失败 - {result.stderr}"
        log("后端 Docker 镜像构建成功")
    except Exception as e:
        return None, port, str(e)

    # 运行容器
    log("正在启动后端容器...")
    try:
        subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
        subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)

        run_cmd = f'docker run -d --name {image_name} -p {port}:8080 {image_name}'
        result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"启动失败 - {result.stderr}"

        # 等待几秒后检查容器状态
        time.sleep(3)
        check_result = subprocess.run(
            f"docker inspect -f '{{{{.State.Running}}}}' {image_name}",
            shell=True, capture_output=True, text=True
        )
        if "true" not in check_result.stdout:
            try:
                logs_result = subprocess.run(
                    ["docker", "logs", "--tail", "50", image_name],
                    capture_output=True, text=True, timeout=10
                )
                container_logs = logs_result.stdout + logs_result.stderr if logs_result.stdout or logs_result.stderr else "无法获取日志"
            except Exception as e:
                container_logs = f"获取日志失败: {str(e)}"
            subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
            subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)
            return None, port, f"容器启动后未运行. 错误日志: {container_logs[:500]}"

        log("后端容器启动成功")
    except Exception as e:
        return None, port, str(e)

    return f"http://{get_host_ip()}:{port}", port, None


def deploy_backend(backend_files, app_id, app_dir, log):
    """部署后端"""
    # 写入后端文件
    main_py_content = None
    for file_item in backend_files:
        filepath = os.path.join(app_dir, file_item['filename'])
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(file_item['content'])

        # 保存 main.py 内容以便添加 CORS
        if file_item['filename'] == 'main.py':
            main_py_content = file_item['content']

    # 检查依赖文件类型
    has_requirements = any(f['filename'] == 'requirements.txt' for f in backend_files)
    has_go_mod = any(f['filename'] == 'go.mod' for f in backend_files)

    if has_go_mod:
        # Go 项目
        return deploy_backend_go(backend_files, app_id, app_dir, log)

    if not has_requirements:
        # 创建默认 requirements.txt
        requirements = """fastapi==0.109.0
uvicorn==0.27.0
"""
        with open(os.path.join(app_dir, "requirements.txt"), "w", encoding="utf-8") as fp:
            fp.write(requirements)

    # 如果有 main.py，确保包含 CORS 支持
    if main_py_content:
        # 检查是否已经包含 CORS
        if 'CORSMiddleware' not in main_py_content:
            # 添加 CORS 支持
            cors_main = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

'''
            # 查找 @app 位置并插入 CORS
            lines = main_py_content.split('\n')
            new_lines = []
            inserted = False
            for line in lines:
                if not inserted and 'from fastapi import' in line and 'FastAPI' in line:
                    new_lines.append(line)
                    new_lines.append('from fastapi.middleware.cors import CORSMiddleware')
                elif not inserted and 'app = FastAPI' in line:
                    new_lines.append(line)
                    new_lines.append('')
                    new_lines.append('# 允许所有来源访问')
                    new_lines.append('app.add_middleware(')
                    new_lines.append('    CORSMiddleware,')
                    new_lines.append('    allow_origins=["*"],')
                    new_lines.append('    allow_credentials=True,')
                    new_lines.append('    allow_methods=["*"],')
                    new_lines.append('    allow_headers=["*"],')
                    new_lines.append(')')
                    inserted = True
                else:
                    new_lines.append(line)

            with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as fp:
                fp.write('\n'.join(new_lines))

    # 创建 Dockerfile
    dockerfile_content = """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    with open(os.path.join(app_dir, "Dockerfile"), "w", encoding="utf-8") as fp:
        fp.write(dockerfile_content)

    # 获取端口
    port = get_app_port()
    image_name = f"ai_web_gen_backend_{app_id}"

    # 构建 Docker 镜像
    log(f"正在构建后端 Docker 镜像 (端口: {port})...")
    try:
        build_cmd = f'docker build -t {image_name} "{app_dir}"'
        result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"构建失败 - {result.stderr}"
        log("后端 Docker 镜像构建成功")
    except Exception as e:
        return None, port, str(e)

    # 运行容器
    log("正在启动后端容器...")
    try:
        # 先停止可能存在的同名容器
        subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
        subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)

        run_cmd = f'docker run -d --name {image_name} -p {port}:8000 {image_name}'
        result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return None, port, f"启动失败 - {result.stderr}"

        # 等待几秒后检查容器状态
        time.sleep(3)
        check_result = subprocess.run(
            f"docker inspect -f '{{{{.State.Running}}}}' {image_name}",
            shell=True, capture_output=True, text=True
        )
        if "true" not in check_result.stdout:
            try:
                logs_result = subprocess.run(
                    ["docker", "logs", "--tail", "50", image_name],
                    capture_output=True, text=True, timeout=10
                )
                container_logs = logs_result.stdout + logs_result.stderr if logs_result.stdout or logs_result.stderr else "无法获取日志"
            except Exception as e:
                container_logs = f"获取日志失败: {str(e)}"
            subprocess.run(f"docker stop {image_name}", shell=True, capture_output=True)
            subprocess.run(f"docker rm {image_name}", shell=True, capture_output=True)
            return None, port, f"容器启动后未运行. 错误日志: {container_logs}"

        log("后端容器启动成功")
    except Exception as e:
        return None, port, str(e)

    return f"http://{get_host_ip()}:{port}", port, None


def generate_deploy_events(request_code: str, request_name: str, db: Session, current_user):
    """生成部署进度事件的 generator"""

    def log(message: str):
        """记录日志"""
        yield json.dumps({"status": "log", "message": message}, ensure_ascii=False) + "\n"

    # 步骤1: 解析代码
    yield from log("正在解析代码...")
    try:
        files = json.loads(request_code)
    except:
        yield from log("错误: 无效的代码格式")
        yield json.dumps({"status": "error", "message": "无效的代码格式"}, ensure_ascii=False) + "\n"
        return

    if not files:
        yield from log("错误: 没有可部署的代码")
        yield json.dumps({"status": "error", "message": "没有可部署的代码"}, ensure_ascii=False) + "\n"
        return

    yield from log(f"解析完成，共 {len(files)} 个文件")

    # 步骤2: 分离前端和后端文件
    frontend_files = []
    backend_files = []

    for f in files:
        filename = f.get('filename', '')
        content = f.get('content', '')
        folder = f.get('folder', 'frontend')

        if folder == 'frontend':
            frontend_files.append({'filename': filename, 'content': content})
        else:
            backend_files.append({'filename': filename, 'content': content})

    yield from log(f"前端文件: {len(frontend_files)}, 后端文件: {len(backend_files)}")

    # 检查是否有已存在的部署，如果有则删除
    existing_deployments = db.query(models.Deployment).filter(
        models.Deployment.user_id == current_user.id
    ).order_by(models.Deployment.created_at.desc()).limit(5).all()

    for existing in existing_deployments:
        # 删除旧的容器和镜像
        old_app_id = existing.id
        old_frontend_container = f"ai_web_gen_frontend_{old_app_id}"
        old_backend_container = f"ai_web_gen_backend_{old_app_id}"

        for container in [old_frontend_container, old_backend_container]:
            try:
                subprocess.run(f"docker stop {container}", shell=True, capture_output=True)
                subprocess.run(f"docker rm {container}", shell=True, capture_output=True)
                subprocess.run(f"docker rmi {container.replace('ai_web_gen_', 'ai_web_gen_')}", shell=True, capture_output=True)
            except:
                pass

        # 删除旧的部署目录
        old_frontend_dir = os.path.join(DEPLOY_BASE_DIR, f"app_{old_app_id}_frontend")
        old_backend_dir = os.path.join(DEPLOY_BASE_DIR, f"app_{old_app_id}_backend")
        if os.path.exists(old_frontend_dir):
            shutil.rmtree(old_frontend_dir, ignore_errors=True)
        if os.path.exists(old_backend_dir):
            shutil.rmtree(old_backend_dir, ignore_errors=True)

    yield from log("已清理旧部署")

    # 创建部署目录
    app_id = int(time.time())

    frontend_url = None
    backend_url = None
    frontend_port = None
    backend_port = None
    deployed_url = None

    # 步骤3: 先部署后端（这样前端部署时知道后端端口）
    if backend_files:
        yield from log("=" * 40)
        yield from log("开始部署后端...")
        backend_dir = os.path.join(DEPLOY_BASE_DIR, f"app_{app_id}_backend")
        os.makedirs(backend_dir, exist_ok=True)

        backend_url, backend_port, error = deploy_backend(backend_files, app_id, backend_dir, lambda m: list(log(m)))

        if error:
            yield from log(f"错误: {error}")
            yield json.dumps({"status": "error", "message": error}, ensure_ascii=False) + "\n"
            # 清理
            if os.path.exists(backend_dir):
                shutil.rmtree(backend_dir, ignore_errors=True)
            return
    else:
        yield from log("没有后端文件，跳过后端部署")

    # 步骤4: 部署前端（后端已部署，可以获取后端端口）
    if frontend_files:
        yield from log("=" * 40)
        yield from log("开始部署前端...")
        frontend_dir = os.path.join(DEPLOY_BASE_DIR, f"app_{app_id}_frontend")
        os.makedirs(frontend_dir, exist_ok=True)

        # 构建后端 URL 用于 nginx 代理（只传端口）
        be_port = str(backend_port) if backend_port else None

        frontend_url, frontend_port, error = deploy_frontend(frontend_files, app_id, frontend_dir, be_port, lambda m: list(log(m)))

        if error:
            yield from log(f"错误: {error}")
            yield json.dumps({"status": "error", "message": error}, ensure_ascii=False) + "\n"
            # 清理
            if os.path.exists(frontend_dir):
                shutil.rmtree(frontend_dir, ignore_errors=True)
            return
    else:
        yield from log("没有前端文件，跳过前端部署")

    # 步骤5: 验证部署
    yield from log("=" * 40)
    yield from log("正在验证部署...")

    deployment_status = "running"
    error_messages = []

    # 验证前端容器
    if frontend_url and frontend_port:
        frontend_container = f"ai_web_gen_frontend_{app_id}"
        try:
            result = subprocess.run(
                f"docker inspect -f '{{{{.State.Running}}}}' {frontend_container}",
                shell=True, capture_output=True, text=True
            )
            if "true" not in result.stdout:
                deployment_status = "failed"
                error_messages.append(f"前端容器未运行")
                yield from log(f"警告: 前端容器未运行")
            else:
                # 尝试访问前端
                import urllib.request
                import urllib.error
                try:
                    urllib.request.urlopen(f"http://192.168.21.6:{frontend_port}", timeout=5)
                    yield from log(f"前端验证成功")
                except Exception as e:
                    yield from log(f"警告: 前端无法访问 - {str(e)[:50]}")
        except Exception as e:
            yield from log(f"前端验证失败: {str(e)[:50]}")

    # 验证后端容器
    if backend_url and backend_port:
        backend_container = f"ai_web_gen_backend_{app_id}"
        try:
            result = subprocess.run(
                f"docker inspect -f '{{{{.State.Running}}}}' {backend_container}",
                shell=True, capture_output=True, text=True
            )
            if "true" not in result.stdout:
                deployment_status = "failed"
                error_messages.append(f"后端容器未运行")
                yield from log(f"警告: 后端容器未运行")
            else:
                # 尝试访问后端健康检查
                import urllib.request
                import urllib.error
                try:
                    # 尝试访问 /health 或根路径
                    urllib.request.urlopen(f"http://192.168.21.6:{backend_port}/", timeout=5)
                    yield from log(f"后端验证成功")
                except urllib.error.HTTPError as e:
                    # 任何 HTTP 响应都说明后端在运行
                    yield from log(f"后端验证成功 (HTTP {e.code})")
                except Exception as e:
                    yield from log(f"警告: 后端无法访问 - {str(e)[:50]}")
        except Exception as e:
            yield from log(f"后端验证失败: {str(e)[:50]}")

    # 步骤6: 完成
    deployed_url = frontend_url or backend_url

    if frontend_url:
        yield from log(f"前端部署完成! 访问地址: {frontend_url}")
    if backend_url:
        yield from log(f"后端部署完成! 访问地址: {backend_url}")

    # 保存部署记录
    deployment = models.Deployment(
        app_name=request_name or f"App_{app_id}",
        code=request_code,
        deployed_url=deployed_url,
        port=frontend_port or backend_port,
        status=deployment_status,
        user_id=current_user.id
    )
    db.add(deployment)
    db.commit()
    db.refresh(deployment)

    if deployment_status == "failed":
        yield json.dumps({
            "status": "completed_with_errors",
            "message": "部署完成但存在错误",
            "error": "; ".join(error_messages),
            "url": deployed_url,
            "frontend_url": frontend_url,
            "backend_url": backend_url,
            "port": frontend_port or backend_port,
            "id": deployment.id
        }, ensure_ascii=False) + "\n"
    else:
        yield json.dumps({
            "status": "completed",
            "message": "部署成功",
            "url": deployed_url,
            "frontend_url": frontend_url,
            "backend_url": backend_url,
            "port": frontend_port or backend_port,
            "id": deployment.id
        }, ensure_ascii=False) + "\n"


@router.post("/deploy/stream")
def deploy_app_stream(
    request: schemas.DeployRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """流式返回部署进度"""
    return StreamingResponse(
        generate_deploy_events(request.code, request.name, db, current_user),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/deployments", response_model=list)
def get_deployments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """获取用户的部署列表"""
    deployments = db.query(models.Deployment).filter(
        models.Deployment.user_id == current_user.id
    ).order_by(models.Deployment.created_at.desc()).all()
    return deployments


@router.delete("/deployments/{deployment_id}")
def delete_deployment(
    deployment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """删除部署"""
    deployment = db.query(models.Deployment).filter(
        models.Deployment.id == deployment_id,
        models.Deployment.user_id == current_user.id
    ).first()

    if not deployment:
        raise HTTPException(status_code=404, detail="部署不存在")

    # 停止并删除容器
    app_id = deployment.id

    # 前端容器
    frontend_container = f"ai_web_gen_frontend_{app_id}"
    try:
        subprocess.run(f"docker stop {frontend_container}", shell=True, capture_output=True)
        subprocess.run(f"docker rm {frontend_container}", shell=True, capture_output=True)
        subprocess.run(f"docker rmi ai_web_gen_frontend_{app_id}", shell=True, capture_output=True)
    except:
        pass

    # 后端容器
    backend_container = f"ai_web_gen_backend_{app_id}"
    try:
        subprocess.run(f"docker stop {backend_container}", shell=True, capture_output=True)
        subprocess.run(f"docker rm {backend_container}", shell=True, capture_output=True)
        subprocess.run(f"docker rmi ai_web_gen_backend_{app_id}", shell=True, capture_output=True)
    except:
        pass

    # 删除部署目录
    frontend_dir = os.path.join(DEPLOY_BASE_DIR, f"app_{app_id}_frontend")
    backend_dir = os.path.join(DEPLOY_BASE_DIR, f"app_{app_id}_backend")
    if os.path.exists(frontend_dir):
        shutil.rmtree(frontend_dir, ignore_errors=True)
    if os.path.exists(backend_dir):
        shutil.rmtree(backend_dir, ignore_errors=True)

    db.delete(deployment)
    db.commit()

    return {"message": "删除成功"}


@router.post("/deployments/{deployment_id}/stop")
def stop_deployment(
    deployment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """暂停部署"""
    deployment = db.query(models.Deployment).filter(
        models.Deployment.id == deployment_id,
        models.Deployment.user_id == current_user.id
    ).first()

    if not deployment:
        raise HTTPException(status_code=404, detail="部署不存在")

    # 停止容器
    app_id = deployment.id

    for container_type in ["frontend", "backend"]:
        container_name = f"ai_web_gen_{container_type}_{app_id}"
        try:
            subprocess.run(f"docker stop {container_name}", shell=True, capture_output=True)
        except:
            pass

    deployment.status = "stopped"
    db.commit()

    return {"message": "暂停成功", "status": "stopped"}


@router.post("/deployments/{deployment_id}/start")
def start_deployment(
    deployment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """启动/恢复部署"""
    deployment = db.query(models.Deployment).filter(
        models.Deployment.id == deployment_id,
        models.Deployment.user_id == current_user.id
    ).first()

    if not deployment:
        raise HTTPException(status_code=404, detail="部署不存在")

    app_id = deployment.id

    # 启动容器
    started = False
    for container_type in ["frontend", "backend"]:
        container_name = f"ai_web_gen_{container_type}_{app_id}"
        try:
            # 检查容器是否存在
            result = subprocess.run(f"docker ps -a --filter name={container_name} --format {{{{.Names}}}}",
                                    shell=True, capture_output=True, text=True)
            if container_name in result.stdout:
                subprocess.run(f"docker start {container_name}", shell=True, capture_output=True)
                started = True
        except:
            pass

    if started:
        deployment.status = "running"
        db.commit()
        return {"message": "启动成功", "status": "running"}
    else:
        return {"message": "容器不存在，需要重新部署", "status": "not_found"}


@router.get("/deployments/{deployment_id}/status")
def get_deployment_status(
    deployment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """获取部署状态"""
    deployment = db.query(models.Deployment).filter(
        models.Deployment.id == deployment_id,
        models.Deployment.user_id == current_user.id
    ).first()

    if not deployment:
        raise HTTPException(status_code=404, detail="部署不存在")

    # 检查容器实际状态
    app_id = deployment.id
    actual_status = "unknown"

    for container_type in ["frontend", "backend"]:
        container_name = f"ai_web_gen_{container_type}_{app_id}"
        try:
            result = subprocess.run(f"docker ps --filter name={container_name} --format {{{{.Status}}}}",
                                    shell=True, capture_output=True, text=True)
            if result.stdout.strip():
                actual_status = "running"
                break
        except:
            pass

    if actual_status == "running" and deployment.status != "running":
        deployment.status = "running"
        db.commit()
    elif actual_status != "running" and deployment.status == "running":
        deployment.status = "stopped"
        db.commit()

    return {
        "id": deployment.id,
        "app_name": deployment.app_name,
        "status": deployment.status,
        "deployed_url": deployment.deployed_url,
        "port": deployment.port,
        "created_at": deployment.created_at
    }