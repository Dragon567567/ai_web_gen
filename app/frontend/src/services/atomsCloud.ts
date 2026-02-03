import { createClient } from '@metagptx/web-sdk';

// 创建Atoms Cloud客户端
export const client = createClient();

// 用户认证相关
export const auth = {
  // 获取当前用户信息
  async getCurrentUser() {
    try {
      const user = await client.auth.me();
      return user.data;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      return null;
    }
  },

  // 跳转到登录页面
  async toLogin() {
    await client.auth.toLogin();
  },

  // 登录回调处理
  login() {
    return client.auth.login();
  },

  // 退出登录
  async logout() {
    await client.auth.logout();
  }
};

// 项目管理相关（使用Atoms Cloud数据库）
export const projects = {
  // 查询用户的所有项目
  async list() {
    try {
      const response = await client.entities.projects.query({
        query: {},
        sort: '-created_at',
        limit: 50
      });
      return response.data.items;
    } catch (error) {
      console.error('获取项目列表失败:', error);
      return [];
    }
  },

  // 创建新项目
  async create(data: { name: string; description: string; code: any }) {
    try {
      const response = await client.entities.projects.create({
        data: {
          name: data.name,
          description: data.description,
          html: data.code.html,
          css: data.code.css,
          javascript: data.code.javascript,
          created_at: new Date().toISOString()
        }
      });
      return response.data;
    } catch (error) {
      console.error('创建项目失败:', error);
      throw error;
    }
  },

  // 更新项目
  async update(id: string, data: any) {
    try {
      const response = await client.entities.projects.update({
        id,
        data
      });
      return response.data;
    } catch (error) {
      console.error('更新项目失败:', error);
      throw error;
    }
  },

  // 删除项目
  async delete(id: string) {
    try {
      await client.entities.projects.delete({ id });
    } catch (error) {
      console.error('删除项目失败:', error);
      throw error;
    }
  }
};