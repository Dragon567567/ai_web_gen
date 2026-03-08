import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

interface User {
  id: number
  username: string
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    token.value = response.data.access_token
    user.value = {
      id: response.data.user_id,
      username: response.data.username,
      email: ''
    }
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user_id', String(response.data.user_id))
    localStorage.setItem('username', response.data.username)
  }

  async function register(username: string, email: string, password: string) {
    await api.post('/auth/register', {
      username,
      email,
      password
    })
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
  }

  function initFromStorage() {
    const storedToken = localStorage.getItem('token')
    const storedUserId = localStorage.getItem('user_id')
    const storedUsername = localStorage.getItem('username')

    if (storedToken && storedUserId && storedUsername) {
      token.value = storedToken
      user.value = {
        id: parseInt(storedUserId),
        username: storedUsername,
        email: ''
      }
    }
  }

  initFromStorage()

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout
  }
})
