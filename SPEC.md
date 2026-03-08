# AI Web Code Generator - 项目规格说明书

## 1. 项目概述

- **项目名称**: AI Web Code Generator
- **项目类型**: Web全栈应用
- **核心功能**: 用户可以通过自然语言描述生成Web代码，并发布为独立应用
- **目标用户**: 开发者、非技术人员需要快速生成Web页面的用户

## 2. 技术栈

### 前端
- Vue 3 (Composition API)
- TypeScript
- Element Plus (UI组件库)
- ECharts (数据可视化)
- Vue Router (路由管理)
- Pinia (状态管理)
- Vite (构建工具)

### 后端
- FastAPI (Python Web框架)
- SQLAlchemy (ORM)
- SQLite (数据库)
- Pydantic (数据验证)
- JWT (用户认证)

## 3. 功能列表

### 用户模块
- [x] 用户注册
- [x] 用户登录
- [x] JWT令牌认证
- [x] 用户登出

### 代码生成模块
- [x] 自然语言描述生成代码
- [x] 代码预览
- [x] 代码编辑
- [x] 生成历史记录

### 应用发布模块
- [x] 预览生成的应用
- [x] 发布应用
- [x] 应用列表管理

## 4. UI/UX 设计方向

### 整体风格
- 现代简洁的深色主题
- 科技感强烈的蓝紫渐变配色
- 卡片式布局

### 配色方案
- 主色: #6366f1 (靛蓝色)
- 辅色: #8b5cf6 (紫罗兰色)
- 背景: #0f172a (深蓝黑色)
- 卡片背景: #1e293b (蓝灰色)
- 文字: #f8fafc (浅白色)

### 布局
- 左侧固定导航栏
- 右侧内容区域
- 响应式设计

### 页面结构
1. 登录/注册页 - 独立页面
2. 主应用布局 - 左侧导航 + 右侧内容
3. 代码生成页 - 输入框 + 代码编辑器 + 预览
4. 应用管理页 - 卡片列表展示

## 5. API接口设计

### 认证接口
- POST /api/auth/register - 注册用户
- POST /api/auth/login - 登录
- POST /api/auth/logout - 登出

### 代码生成接口
- POST /api/code/generate - 生成代码
- GET /api/code/history - 获取生成历史

### 应用管理接口
- GET /api/apps - 获取应用列表
- POST /api/apps - 发布应用
- GET /api/apps/{id} - 获取应用详情
- DELETE /api/apps/{id} - 删除应用