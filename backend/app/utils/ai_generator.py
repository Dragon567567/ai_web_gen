import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from zai import ZhipuAiClient

activate_model = "glm-4.7"
client = ZhipuAiClient(api_key="")  # 请填写您自己的 API Key


def review_code(files_json: str, prompt: str) -> str:
    """Review and fix generated code using AI"""

    review_prompt = f"""你是一个专业的代码审查员。请审查并修复以下生成的代码中的错误。

用户需求：{prompt}

生成的代码：
{files_json}

请检查以下方面：
1. 语法错误
2. 逻辑错误
3. 缺失的依赖
4. 安全隐患
5. HTML/CSS/JS 标签是否匹配
6. JSON 格式是否正确

请只返回修复后的JSON数组，不要有其他解释文字。格式与输入相同，每个元素包含 filename、content 和 folder 字段。"""

    try:
        response = client.chat.completions.create(
            model=activate_model,
            messages=[
                {"role": "system", "content": "你是一个专业的代码审查员，擅长发现和修复代码中的错误。"},
                {"role": "user", "content": review_prompt}
            ],
            thinking={
                "type": "enabled",  # 启用深度思考模式
            },
        )

        reviewed_code = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if reviewed_code.startswith("```json"):
            reviewed_code = reviewed_code[7:]
        elif reviewed_code.startswith("```"):
            reviewed_code = reviewed_code[3:]
        if reviewed_code.endswith("```"):
            reviewed_code = reviewed_code[:-3]

        # Validate JSON
        json.loads(reviewed_code.strip())

        return reviewed_code.strip()

    except Exception as e:
        # If review fails, return original code
        print(f"Code review failed: {e}")
        return files_json


def fix_json_error(generated_code: str, prompt: str) -> str:
    """Fix JSON parsing errors using AI"""

    fix_prompt = f"""你是一个JSON修复专家。以下是生成的代码，但它不是有效的JSON格式。请修复它使其成为有效的JSON数组格式。

用户需求：{prompt}

生成的代码（无效的JSON）：
{generated_code}

请只返回修复后的有效JSON数组，不要有其他解释文字。每个元素需要包含 filename、content 和 folder 字段。"""

    try:
        response = client.chat.completions.create(
            model=activate_model,
            messages=[
                {"role": "system", "content": "你是一个JSON修复专家，擅长修复格式错误的JSON。"},
                {"role": "user", "content": fix_prompt}
            ],
            thinking={
                "type": "enabled",  # 启用深度思考模式
            },
        )

        fixed_code = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if fixed_code.startswith("```json"):
            fixed_code = fixed_code[7:]
        elif fixed_code.startswith("```"):
            fixed_code = fixed_code[3:]
        if fixed_code.endswith("```"):
            fixed_code = fixed_code[:-3]

        # Validate the fixed JSON
        json.loads(fixed_code.strip())

        return fixed_code.strip()

    except Exception as e:
        # If fix fails, raise the original error
        raise ValueError(f"Failed to fix JSON: {e}")


def generate_code(prompt: str) -> str:
    """Generate full-stack code using OpenAI API based on user prompt"""

    system_prompt = """你是一个专业的全栈Web开发者。请根据用户的描述生成完整的Web项目代码，包括前端和后端。

要求：
1. 生成完整的、前后端分离的项目代码，包含前端和后端
2. 前端：HTML、CSS、JavaScript/TypeScript、Vue/React组件等
3. 后端：Python (FastAPI/Flask)、Node.js、Go 等
4. 每个文件要有合适的文件名（使用英文）
5. 文件内容要完整、可运行
6. 后端代码使用 FastAPI 框架优先
7. 如果需要数据库，提供完整的数据库模型和迁移脚本
8. 页面要美观、响应式、用户体验好
9. 如果用户用中文描述，请用中文生成页面内容
10. 只返回JSON数据，不要有其他解释文字
11. 返回格式为JSON数组，每个元素包含 filename 和 content 字段
12. 使用 folder 字段标识文件所属目录，例如：{"filename": "main.py", "content": "...", "folder": "backend"}
13. 如果需要安装依赖，生成的文件里要有前后端的依赖文件

示例：
[
  {"filename": "index.html", "content": "<!DOCTYPE html>...", "folder": "frontend"},
  {"filename": "style.css", "content": "body {...}", "folder": "frontend"},
  {"filename": "app.js", "content": "console.log(...)", "folder": "frontend"},
  {"filename": "main.py", "content": "from fastapi import...", "folder": "backend"},
  {"filename": "models.py", "content": "class User...", "folder": "backend"}
]"""

    try:
        response = client.chat.completions.create(
            model=activate_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            thinking={
                "type": "enabled",  # 启用深度思考模式
            },
        )

        # 获取完整回复
        generated_code = response.choices[0].message.content.strip()

        # Remove any markdown code blocks if present
        if generated_code.startswith("```json"):
            generated_code = generated_code[7:]
        elif generated_code.startswith("```"):
            generated_code = generated_code[3:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]

        # Try to validate JSON, if fails, use AI to fix
        try:
            files = json.loads(generated_code.strip())
        except json.JSONDecodeError:
            # If JSON is invalid, use AI to fix it
            fixed_code = fix_json_error(generated_code, prompt)
            files = json.loads(fixed_code.strip())

        # Ensure it's a list
        if isinstance(files, dict):
            files = [files]

        # Add folder field if not present
        for f in files:
            if 'folder' not in f:
                # Guess folder based on file extension
                if f.get('filename', '').endswith(('.html', '.css', '.js', '.ts', '.vue', '.jsx', '.tsx')):
                    f['folder'] = 'frontend'
                else:
                    f['folder'] = 'backend'

        # Convert back to JSON string for review
        files_json = json.dumps(files, ensure_ascii=False)

        # Review and fix code
        reviewed_code = review_code(files_json, prompt)

        # Validate JSON after review
        try:
            reviewed_files = json.loads(reviewed_code)
            # Ensure it's a list
            if isinstance(reviewed_files, dict):
                reviewed_files = [reviewed_files]
            # Add folder field if not present
            for f in reviewed_files:
                if 'folder' not in f:
                    if f.get('filename', '').endswith(('.html', '.css', '.js', '.ts', '.vue', '.jsx', '.tsx')):
                        f['folder'] = 'frontend'
                    else:
                        f['folder'] = 'backend'
            reviewed_code = json.dumps(reviewed_files, ensure_ascii=False)
        except json.JSONDecodeError:
            # If review result is invalid, return original
            return files_json

        return reviewed_code

    except Exception as e:
        # Fallback to a simple error page if API fails
        error_page = {
            "filename": "index.html",
            "content": f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成失败</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            max-width: 500px;
        }}
        h1 {{ color: #333; }}
        p {{ color: #666; margin: 20px 0; }}
        .error {{ color: #ef4444; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>生成失败</h1>
        <p class="error">抱歉，代码生成服务暂时不可用。</p>
        <p>错误信息: {str(e)[:100]}</p>
    </div>
</body>
</html>''',
            "folder": "frontend"
        }
        return json.dumps([error_page], ensure_ascii=False)


def modify_code(original_code: str, feedback: str) -> str:
    """根据用户反馈修改代码"""

    modify_prompt = f"""你是一个专业的Web开发者。请根据用户的反馈修改以下代码。

原始代码：
{original_code}

用户反馈：
{feedback}

请根据用户反馈修改代码，只返回修改后的JSON数组格式，不要有其他解释文字。每个元素需要包含 filename、content 和 folder 字段。

注意：
1. 只修改需要修改的部分，不要完全重写
2. 保持其他文件不变
3. 返回完整的JSON数组，包含所有文件"""

    try:
        response = client.chat.completions.create(
            model=activate_model,
            messages=[
                {"role": "system", "content": "你是一个专业的Web开发者，擅长根据用户反馈修改代码。"},
                {"role": "user", "content": modify_prompt}
            ],
            thinking={
                "type": "enabled",  # 启用深度思考模式
            },
        )

        modified_code = response.choices[0].message.content.strip()

        # Remove markdown code blocks if present
        if modified_code.startswith("```json"):
            modified_code = modified_code[7:]
        elif modified_code.startswith("```"):
            modified_code = modified_code[3:]
        if modified_code.endswith("```"):
            modified_code = modified_code[:-3]

        # Validate JSON
        files = json.loads(modified_code.strip())

        # Ensure it's a list
        if isinstance(files, dict):
            files = [files]

        # Add folder field if not present
        for f in files:
            if 'folder' not in f:
                if f.get('filename', '').endswith(('.html', '.css', '.js', '.ts', '.vue', '.jsx', '.tsx')):
                    f['folder'] = 'frontend'
                else:
                    f['folder'] = 'backend'

        return json.dumps(files, ensure_ascii=False)

    except Exception as e:
        # If modification fails, return original code
        print(f"Code modification failed: {e}")
        return original_code
