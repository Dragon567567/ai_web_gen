// src/utils/request.js
import axios from 'axios'

// 创建 axios 实例
const service = axios.create({
  // 基础请求地址（根据你的后端接口域名配置）
  baseURL: '/api/v1',
  // 请求超时时间（毫秒）
  timeout: 180000,
  // 请求头默认配置
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器：发送请求前做些处理（比如添加 token）
service.interceptors.request.use(
  (config) => {
    // 示例：从本地存储获取 token 并添加到请求头
    return config
  },
  (error) => {
    // 请求错误的处理
    console.error('请求拦截器错误：', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：接收响应后做些处理（比如统一处理错误）
service.interceptors.response.use(
  (response) => {
    // 解构响应数据（根据你的后端返回格式调整）
    const { data } = response
    // 示例：后端返回 code !== 200 视为业务错误
    if (data.code !== 0) {
      // 可结合 Element Plus 等 UI 库提示错误
      // ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg || '请求失败'))
    }
    // 只返回核心数据，简化组件内使用
    return data.data
  },
  (error) => {
    // HTTP 状态码错误处理（401、403、500 等）
    console.error('响应拦截器错误：', error)
    const status = error.response?.status
    switch (status) {
      case 401:
        // 未授权：清除 token 并跳转到登录页
        localStorage.removeItem('token')
        window.location.href = '/login'
        break
      case 403:
        // 权限不足
        // ElMessage.error('暂无权限访问')
        break
      case 500:
        // 服务器错误
        // ElMessage.error('服务器内部错误，请稍后重试')
        break
      default:
        // ElMessage.error(error.message || '请求出错')
        break
    }
    return Promise.reject(error)
  }
)

// 导出封装后的 axios 实例
export default service