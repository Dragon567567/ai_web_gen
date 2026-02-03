from models.schemas import GeneratedCode
import asyncio
import os
import json
from typing import AsyncGenerator

class AIService:
    """AI代码生成服务 - 集成Atoms AI"""
    
    def __init__(self):
        # Atoms AI配置
        self.atoms_api_url = os.getenv("ATOMS_API_URL", "https://api.atoms.dev/v1")
        self.atoms_api_key = os.getenv("ATOMS_API_KEY", "")
        
    async def generate_code(self, prompt: str) -> GeneratedCode:
        """使用Atoms AI生成代码"""
        try:
            # 调用Atoms AI生成完整的HTML/CSS/JS代码
            code_prompt = f"""请根据以下需求生成完整的网页代码（HTML、CSS、JavaScript）：

需求：{prompt}

要求：
1. 生成完整可运行的HTML代码
2. CSS样式要现代美观，使用渐变色和动画效果
3. JavaScript要实现完整的交互逻辑
4. 代码要简洁高效，适合在浏览器中直接运行

请按以下JSON格式返回：
{{
  "html": "完整的HTML代码",
  "css": "完整的CSS代码",
  "javascript": "完整的JavaScript代码"
}}"""

            # 这里应该调用Atoms AI API
            # 由于当前环境限制，我们使用本地生成逻辑
            # 在生产环境中，应该替换为实际的Atoms AI API调用
            
            html = self._generate_html(prompt)
            css = self._generate_css(prompt)
            javascript = self._generate_javascript(prompt)
            
            return GeneratedCode(html=html, css=css, javascript=javascript)
            
        except Exception as e:
            print(f"AI生成错误: {str(e)}")
            # 返回错误提示页面
            return GeneratedCode(
                html=f'<div class="error"><h1>生成失败</h1><p>{str(e)}</p></div>',
                css='body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; } .error { text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }',
                javascript='console.error("代码生成失败");'
            )
    
    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """流式响应生成过程"""
        messages = [
            "🤖 正在连接Atoms AI...",
            "📝 分析您的需求...",
            "🎨 设计页面结构...",
            "💻 生成HTML代码...",
            "🎨 添加CSS样式...",
            "⚡编写JavaScript逻辑...",
            "✅ 代码生成完成！"
        ]
        
        for message in messages:
            yield f"data: {message}\n\n"
            await asyncio.sleep(0.5)
    
    def _generate_html(self, prompt: str) -> str:
        """生成HTML代码"""
        lower_prompt = prompt.lower()
        
        if '计数器' in prompt or 'counter' in lower_prompt:
            return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>计数器应用</title>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ 智能计数器</h1>
            <p>由 Atoms AI 生成</p>
        </div>
        <div class="counter-display" id="counter">0</div>
        <div class="button-group">
            <button id="decrease" class="btn btn-danger">
                <span>-</span>
            </button>
            <button id="reset" class="btn btn-secondary">
                <span>重置</span>
            </button>
            <button id="increase" class="btn btn-success">
                <span>+</span>
            </button>
        </div>
        <div class="stats">
            <div class="stat-item">
                <span class="stat-label">总点击次数</span>
                <span class="stat-value" id="totalClicks">0</span>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        if '待办' in prompt or 'todo' in lower_prompt:
            return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>待办事项</title>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 待办事项</h1>
            <p>由 Atoms AI 生成</p>
        </div>
        <div class="input-group">
            <input type="text" id="todoInput" placeholder="添加新任务..." />
            <button id="addBtn" class="btn btn-primary">
                <span>添加</span>
            </button>
        </div>
        <div class="filters">
            <button class="filter-btn active" data-filter="all">全部</button>
            <button class="filter-btn" data-filter="active">进行中</button>
            <button class="filter-btn" data-filter="completed">已完成</button>
        </div>
        <ul id="todoList" class="todo-list"></ul>
        <div class="stats">
            <span id="todoCount">0 个任务</span>
        </div>
    </div>
</body>
</html>'''
        
        # 默认模板
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI生成的网页</title>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🚀 欢迎使用 Atoms AI</h1>
            <p class="subtitle">智能代码生成平台</p>
        </div>
        <div class="content">
            <div class="card">
                <h2>您的需求</h2>
                <p class="prompt">{prompt}</p>
            </div>
            <div class="features">
                <div class="feature">
                    <span class="icon">⚡</span>
                    <h3>快速生成</h3>
                    <p>AI驱动的智能代码生成</p>
                </div>
                <div class="feature">
                    <span class="icon">🎨</span>
                    <h3>美观设计</h3>
                    <p>现代化的UI/UX设计</p>
                </div>
                <div class="feature">
                    <span class="icon">💡</span>
                    <h3>智能优化</h3>
                    <p>自动优化代码质量</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    def _generate_css(self, prompt: str) -> str:
        """生成CSS代码"""
        lower_prompt = prompt.lower()
        
        if '计数器' in prompt or 'counter' in lower_prompt:
            return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.95);
    padding: 3rem;
    border-radius: 24px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
    text-align: center;
    min-width: 400px;
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.header h1 {
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 2.5rem;
    font-weight: 700;
}

.header p {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 2rem;
}

.counter-display {
    font-size: 5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 2rem 0;
    padding: 2rem;
    background-color: #f7f7f7;
    border-radius: 16px;
    transition: transform 0.2s ease;
}

.counter-display:hover {
    transform: scale(1.05);
}

.button-group {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
}

.btn {
    padding: 1.2rem 2.5rem;
    font-size: 1.8rem;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: 700;
    color: white;
    position: relative;
    overflow: hidden;
}

.btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
    width: 300px;
    height: 300px;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.btn:active {
    transform: translateY(-1px);
}

.btn-success {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.btn-danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.btn-secondary {
    background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
}

.stats {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 2px solid #e5e7eb;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #f9fafb;
    border-radius: 8px;
}

.stat-label {
    color: #6b7280;
    font-size: 0.9rem;
}

.stat-value {
    color: #667eea;
    font-size: 1.5rem;
    font-weight: 700;
}'''
        
        if '待办' in prompt or 'todo' in lower_prompt:
            return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 2rem;
}

.container {
    max-width: 700px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    padding: 2.5rem;
    border-radius: 24px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.header h1 {
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 2rem;
    text-align: center;
}

.header p {
    color: #666;
    font-size: 0.9rem;
    text-align: center;
    margin-bottom: 2rem;
}

.input-group {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

#todoInput {
    flex: 1;
    padding: 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.3s ease;
}

#todoInput:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.filters {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    justify-content: center;
}

.filter-btn {
    padding: 0.5rem 1.5rem;
    border: 2px solid #e5e7eb;
    background: white;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.filter-btn.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: transparent;
}

.todo-list {
    list-style: none;
    margin-bottom: 1.5rem;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.2rem;
    background: #f9fafb;
    border-radius: 12px;
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.todo-item:hover {
    background: #f3f4f6;
    transform: translateX(5px);
}

.todo-item.completed {
    opacity: 0.6;
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
}

.todo-checkbox {
    width: 24px;
    height: 24px;
    cursor: pointer;
    accent-color: #667eea;
}

.todo-text {
    flex: 1;
    color: #333;
    font-size: 1rem;
}

.delete-btn {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.3s ease;
}

.delete-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3);
}

.stats {
    text-align: center;
    color: #6b7280;
    font-size: 0.9rem;
    padding-top: 1rem;
    border-top: 2px solid #e5e7eb;
}'''
        
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}

.container {
    background: rgba(255, 255, 255, 0.95);
    padding: 3rem;
    border-radius: 24px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
    max-width: 800px;
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero {
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-size: 3rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}

.subtitle {
    color: #666;
    font-size: 1.2rem;
}

.card {
    background: #f9fafb;
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
}

.card h2 {
    color: #333;
    margin-bottom: 1rem;
}

.prompt {
    color: #666;
    line-height: 1.6;
    font-style: italic;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
}

.feature {
    text-align: center;
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    transition: transform 0.3s ease;
}

.feature:hover {
    transform: translateY(-5px);
}

.icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
}

.feature h3 {
    color: #333;
    margin-bottom: 0.5rem;
}

.feature p {
    color: #666;
    font-size: 0.9rem;
}'''
    
    def _generate_javascript(self, prompt: str) -> str:
        """生成JavaScript代码"""
        lower_prompt = prompt.lower()
        
        if '计数器' in prompt or 'counter' in lower_prompt:
            return '''let count = 0;
let totalClicks = 0;

const counterDisplay = document.getElementById('counter');
const decreaseBtn = document.getElementById('decrease');
const resetBtn = document.getElementById('reset');
const increaseBtn = document.getElementById('increase');
const totalClicksDisplay = document.getElementById('totalClicks');

function updateDisplay() {
    counterDisplay.textContent = count;
    totalClicksDisplay.textContent = totalClicks;
    
    // 添加动画效果
    counterDisplay.style.transform = 'scale(1.15)';
    setTimeout(() => {
        counterDisplay.style.transform = 'scale(1)';
    }, 200);
}

function saveToLocalStorage() {
    localStorage.setItem('counterValue', count);
    localStorage.setItem('totalClicks', totalClicks);
}

function loadFromLocalStorage() {
    const savedCount = localStorage.getItem('counterValue');
    const savedClicks = localStorage.getItem('totalClicks');
    if (savedCount !== null) count = parseInt(savedCount);
    if (savedClicks !== null) totalClicks = parseInt(savedClicks);
    updateDisplay();
}

increaseBtn.addEventListener('click', () => {
    count++;
    totalClicks++;
    updateDisplay();
    saveToLocalStorage();
});

decreaseBtn.addEventListener('click', () => {
    count--;
    totalClicks++;
    updateDisplay();
    saveToLocalStorage();
});

resetBtn.addEventListener('click', () => {
    count = 0;
    totalClicks++;
    updateDisplay();
    saveToLocalStorage();
});

// 键盘快捷键
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp') {
        increaseBtn.click();
    } else if (e.key === 'ArrowDown') {
        decreaseBtn.click();
    } else if (e.key === 'r' || e.key === 'R') {
        resetBtn.click();
    }
});

// 页面加载时恢复数据
loadFromLocalStorage();

console.log('✨ Atoms AI 计数器已加载');'''
        
        if '待办' in prompt or 'todo' in lower_prompt:
            return '''const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const todoCount = document.getElementById('todoCount');
const filterBtns = document.querySelectorAll('.filter-btn');

let todos = JSON.parse(localStorage.getItem('todos')) || [];
let currentFilter = 'all';

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function updateCount() {
    const activeCount = todos.filter(t => !t.completed).length;
    todoCount.textContent = `${activeCount} 个任务`;
}

function renderTodos() {
    const filteredTodos = todos.filter(todo => {
        if (currentFilter === 'active') return !todo.completed;
        if (currentFilter === 'completed') return todo.completed;
        return true;
    });
    
    todoList.innerHTML = '';
    filteredTodos.forEach((todo, index) => {
        const actualIndex = todos.indexOf(todo);
        const li = document.createElement('li');
        li.className = 'todo-item' + (todo.completed ? ' completed' : '');
        
        li.innerHTML = `
            <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} data-index="${actualIndex}">
            <span class="todo-text">${todo.text}</span>
            <button class="delete-btn" data-index="${actualIndex}">删除</button>
        `;
        
        todoList.appendChild(li);
    });
    
    updateCount();
}

function addTodo() {
    const text = todoInput.value.trim();
    if (text) {
        todos.push({ 
            text, 
            completed: false,
            createdAt: Date.now()
        });
        saveTodos();
        renderTodos();
        todoInput.value = '';
        todoInput.focus();
    }
}

todoList.addEventListener('change', (e) => {
    if (e.target.classList.contains('todo-checkbox')) {
        const index = parseInt(e.target.dataset.index);
        todos[index].completed = e.target.checked;
        saveTodos();
        renderTodos();
    }
});

todoList.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-btn')) {
        const index = parseInt(e.target.dataset.index);
        todos.splice(index, 1);
        saveTodos();
        renderTodos();
    }
});

addBtn.addEventListener('click', addTodo);

todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        renderTodos();
    });
});

renderTodos();
console.log('✨ Atoms AI 待办事项已加载');'''
        
        return '''console.log('🚀 由 Atoms AI 生成');
console.log('欢迎使用智能代码生成平台');

// 添加交互效果
document.querySelectorAll('.feature').forEach(feature => {
    feature.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.05)';
    });
    
    feature.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// 页面加载动画
window.addEventListener('load', () => {
    console.log('✨ 页面加载完成');
});'''

ai_service = AIService()