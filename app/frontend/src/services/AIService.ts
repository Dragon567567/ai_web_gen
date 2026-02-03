import { GeneratedCode } from '@/types';

class AIService {
  private apiKey: string = '';

  // 模拟AI代码生成（实际应用中需要集成真实的AI API）
  async generateCode(prompt: string): Promise<GeneratedCode> {
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 2000));

    // 根据提示生成简单的代码示例
    const html = this.generateHTML(prompt);
    const css = this.generateCSS(prompt);
    const javascript = this.generateJavaScript(prompt);

    return { html, css, javascript };
  }

  private generateHTML(prompt: string): string {
    const lowerPrompt = prompt.toLowerCase();
    
    if (lowerPrompt.includes('计数器') || lowerPrompt.includes('counter')) {
      return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>计数器应用</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>计数器</h1>
        <div class="counter-display" id="counter">0</div>
        <div class="button-group">
            <button id="decrease" class="btn btn-danger">-</button>
            <button id="reset" class="btn btn-secondary">重置</button>
            <button id="increase" class="btn btn-success">+</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>`;
    }

    if (lowerPrompt.includes('待办') || lowerPrompt.includes('todo')) {
      return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>待办事项</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>待办事项列表</h1>
        <div class="input-group">
            <input type="text" id="todoInput" placeholder="添加新任务...">
            <button id="addBtn" class="btn btn-primary">添加</button>
        </div>
        <ul id="todoList" class="todo-list"></ul>
    </div>
    <script src="script.js"></script>
</body>
</html>`;
    }

    // 默认模板
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI生成的网页</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>欢迎使用AI代码生成器</h1>
        <p>这是根据您的需求生成的网页应用</p>
        <p class="prompt">您的需求: ${prompt}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>`;
  }

  private generateCSS(prompt: string): string {
    const lowerPrompt = prompt.toLowerCase();

    if (lowerPrompt.includes('计数器') || lowerPrompt.includes('counter')) {
      return `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    text-align: center;
    min-width: 350px;
}

h1 {
    color: #333;
    margin-bottom: 2rem;
    font-size: 2rem;
}

.counter-display {
    font-size: 4rem;
    font-weight: bold;
    color: #667eea;
    margin: 2rem 0;
    padding: 1rem;
    background: #f7f7f7;
    border-radius: 10px;
}

.button-group {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.btn {
    padding: 1rem 2rem;
    font-size: 1.5rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: bold;
    color: white;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-success {
    background: #10b981;
}

.btn-danger {
    background: #ef4444;
}

.btn-secondary {
    background: #6b7280;
}`;
    }

    if (lowerPrompt.includes('待办') || lowerPrompt.includes('todo')) {
      return `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 2rem;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
}

.input-group {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

#todoInput {
    flex: 1;
    padding: 0.75rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
}

#todoInput:focus {
    outline: none;
    border-color: #667eea;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5568d3;
}

.todo-list {
    list-style: none;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: #f9fafb;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    transition: all 0.3s ease;
}

.todo-item:hover {
    background: #f3f4f6;
}

.todo-item.completed {
    opacity: 0.6;
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
}

.todo-checkbox {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

.todo-text {
    flex: 1;
    color: #333;
}

.delete-btn {
    background: #ef4444;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
}

.delete-btn:hover {
    background: #dc2626;
}`;
    }

    return `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}

.container {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    max-width: 600px;
}

h1 {
    color: #333;
    margin-bottom: 1rem;
}

p {
    color: #666;
    line-height: 1.6;
    margin-bottom: 0.5rem;
}

.prompt {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #f7f7f7;
    border-radius: 8px;
    font-style: italic;
}`;
  }

  private generateJavaScript(prompt: string): string {
    const lowerPrompt = prompt.toLowerCase();

    if (lowerPrompt.includes('计数器') || lowerPrompt.includes('counter')) {
      return `let count = 0;

const counterDisplay = document.getElementById('counter');
const decreaseBtn = document.getElementById('decrease');
const resetBtn = document.getElementById('reset');
const increaseBtn = document.getElementById('increase');

function updateDisplay() {
    counterDisplay.textContent = count;
    counterDisplay.style.transform = 'scale(1.1)';
    setTimeout(() => {
        counterDisplay.style.transform = 'scale(1)';
    }, 200);
}

increaseBtn.addEventListener('click', () => {
    count++;
    updateDisplay();
});

decreaseBtn.addEventListener('click', () => {
    count--;
    updateDisplay();
});

resetBtn.addEventListener('click', () => {
    count = 0;
    updateDisplay();
});`;
    }

    if (lowerPrompt.includes('待办') || lowerPrompt.includes('todo')) {
      return `const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');

let todos = JSON.parse(localStorage.getItem('todos')) || [];

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function renderTodos() {
    todoList.innerHTML = '';
    todos.forEach((todo, index) => {
        const li = document.createElement('li');
        li.className = 'todo-item' + (todo.completed ? ' completed' : '');
        
        li.innerHTML = \`
            <input type="checkbox" class="todo-checkbox" \${todo.completed ? 'checked' : ''}>
            <span class="todo-text">\${todo.text}</span>
            <button class="delete-btn">删除</button>
        \`;
        
        const checkbox = li.querySelector('.todo-checkbox');
        checkbox.addEventListener('change', () => {
            todos[index].completed = checkbox.checked;
            saveTodos();
            renderTodos();
        });
        
        const deleteBtn = li.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', () => {
            todos.splice(index, 1);
            saveTodos();
            renderTodos();
        });
        
        todoList.appendChild(li);
    });
}

function addTodo() {
    const text = todoInput.value.trim();
    if (text) {
        todos.push({ text, completed: false });
        saveTodos();
        renderTodos();
        todoInput.value = '';
    }
}

addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

renderTodos();`;
    }

    return `console.log('AI生成的网页已加载');
console.log('用户需求:', '${prompt}');

document.addEventListener('DOMContentLoaded', () => {
    console.log('页面加载完成');
});`;
  }

  // 流式响应模拟
  async *streamResponse(prompt: string): AsyncGenerator<string> {
    const messages = [
      '正在分析您的需求...',
      '理解需求完成，开始生成代码结构...',
      '生成HTML结构中...',
      '添加CSS样式...',
      '编写JavaScript逻辑...',
      '代码生成完成！正在准备预览...'
    ];

    for (const message of messages) {
      yield message;
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
}

export const aiService = new AIService();