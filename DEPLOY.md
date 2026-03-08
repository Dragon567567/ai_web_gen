# AI Web Generator - Docker 部署指南

## 前置要求

- Docker Desktop for Windows 已安装并运行
- 端口 80、3306、8000 可用

## 快速启动

### 1. 启动所有服务

在项目根目录下运行：

```bash
docker-compose up -d
```

这将启动：
- MySQL 数据库 (端口 3306)
- 后端 API (端口 8000)
- 前端 Web (端口 80)

### 2. 访问应用

- 前端: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 3. 查看日志

```bash
docker-compose logs -f
```

### 4. 停止服务

```bash
docker-compose down
```

### 5. 重新构建

如果修改了代码，需要重新构建：

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 环境变量

可以在 `docker-compose.yml` 中修改以下环境变量：

- `DB_HOST`: 数据库主机 (默认: mysql)
- `DB_PORT`: 数据库端口 (默认: 3306)
- `DB_USER`: 数据库用户 (默认: ai_web_gen)
- `DB_PASSWORD`: 数据库密码 (默认: ai_web_gen123)
- `DB_NAME`: 数据库名称 (默认: ai_web_gen)

## 外部访问

要让外界 IP 访问，需要修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "80:80"    # 改为 "外部端口:80"
  - "8000:8000" # 改为 "外部端口:8000"
```

然后在防火墙中开放对应的外部端口。

## 故障排除

### 查看容器状态
```bash
docker-compose ps
```

### 查看特定服务日志
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
```

### 重置数据库
```bash
docker-compose down -v
docker-compose up -d
```