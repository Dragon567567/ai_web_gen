# AI代码生成平台开发计划

## 设计指南

### 设计参考
- **主要灵感**: Atoms.dev, Cursor AI, v0.dev
- **风格**: 现代极简 + 深色主题 + AI驱动界面

### 色彩方案
- Primary: #0A0A0A (深黑 - 背景)
- Secondary: #1A1A1A (炭灰 - 卡片/面板)
- Accent: #6366F1 (靛蓝 - AI主题色/按钮)
- Success: #10B981 (绿色 - 成功状态)
- Text: #FFFFFF (白色), #9CA3AF (浅灰 - 次要文本)
- Border: #2A2A2A (边框色)

### 字体排版
- Heading1: Inter font-weight 700 (32px)
- Heading2: Inter font-weight 600 (24px)
- Heading3: Inter font-weight 600 (18px)
- Body: Inter font-weight 400 (14px)
- Code: JetBrains Mono font-weight 400 (13px)

### 关键组件样式
- **按钮**: 靛蓝背景(#6366F1)，白色文字，8px圆角，悬停时亮度+10%
- **卡片**: 炭灰背景(#1A1A1A)，1px边框(#2A2A2A)，12px圆角
- **输入框**: 深色背景，底部边框，聚焦时靛蓝强调色
- **代码块**: 深色背景，JetBrains Mono字体，语法高亮

### 布局与间距
- 左侧聊天面板: 40%宽度，固定高度
- 右侧预览面板: 60%宽度，可调整大小
- 面板间距: 16px
- 内边距: 24px

### 需要生成的图像
1. **hero-ai-coding.jpg** - AI代码生成概念图，深色科技感 (Style: photorealistic, dark tech)
2. **icon-chat.png** - 聊天图标，简约线条设计 (Style: minimalist, transparent)
3. **icon-code.png** - 代码图标，极简风格 (Style: minimalist, transparent)
4. **icon-preview.png** - 预览图标，现代设计 (Style: minimalist, transparent)

---

## 开发任务

### 1. 项目初始化与结构搭建
- 初始化shadcn-ui模板
- 安装必要依赖
- 创建基础目录结构

### 2. 生成图像资源
- 使用ImageCreator生成所有4张图像

### 3. 核心组件开发
- **ChatPanel.tsx** - 左侧聊天界面组件
  - 消息列表显示
  - 输入框和发送按钮
  - 流式消息渲染
  
- **PreviewPanel.tsx** - 右侧预览面板组件
  - iframe沙箱预览
  - 刷新和全屏功能
  
- **CodeEditor.tsx** - 代码编辑器组件
  - 语法高亮显示
  - 代码复制功能
  
- **AIService.ts** - AI服务集成
  - API调用封装
  - 代码生成逻辑

### 4. 主页面集成
- **App.tsx** - 主应用页面
  - 布局管理
  - 状态管理
  - 组件集成

### 5. 样式与交互优化
- 应用设计系统
- 添加动画效果
- 响应式适配

### 6. 测试与部署
- Lint检查
- 构建测试
- UI渲染验证