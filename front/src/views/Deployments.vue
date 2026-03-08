<template>
  <div class="deployments-container">
    <div class="header">
      <h1>我的部署</h1>
      <p>管理您部署的所有应用</p>
    </div>

    <div class="deployments-grid" v-loading="loading">
      <el-empty v-if="!loading && deploymentsList.length === 0" description="暂无部署" />
      <div
        v-for="deployment in deploymentsList"
        :key="deployment.id"
        :class="['deployment-card', { stopped: deployment.status === 'stopped' }]"
      >
        <div class="deployment-header">
          <div class="app-name">
            <span class="status-dot" :class="deployment.status"></span>
            {{ deployment.app_name }}
          </div>
          <el-tag :type="deployment.status === 'running' ? 'success' : 'danger'" size="small">
            {{ deployment.status === 'running' ? '运行中' : '已暂停' }}
          </el-tag>
        </div>

        <div class="deployment-url">
          <span class="url-label">访问地址：</span>
          <a :href="deployment.deployed_url" target="_blank" class="url-link">
            {{ deployment.deployed_url }}
          </a>
        </div>

        <div class="deployment-meta">
          <span>端口：{{ deployment.port }}</span>
          <span>创建时间：{{ formatDate(deployment.created_at) }}</span>
        </div>

        <div class="deployment-actions">
          <el-button
            v-if="deployment.status === 'running'"
            size="small"
            @click="handleStop(deployment)"
          >
            <el-icon><VideoPause /></el-icon>
            暂停
          </el-button>
          <el-button
            v-else
            type="success"
            size="small"
            @click="handleStart(deployment)"
          >
            <el-icon><VideoPlay /></el-icon>
            启动
          </el-button>
          <el-button type="primary" size="small" @click="handleVisit(deployment)">
            <el-icon><Link /></el-icon>
            访问
          </el-button>
          <el-button type="danger" size="small" @click="handleDelete(deployment)">
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

interface DeploymentItem {
  id: number
  app_name: string
  deployed_url: string
  port: number
  status: string
  created_at: string
}

const router = useRouter()

const deploymentsList = ref<DeploymentItem[]>([])
const loading = ref(false)

async function fetchDeployments() {
  loading.value = true
  try {
    const response = await api.get('/deploy/deployments')
    deploymentsList.value = response.data || []
  } catch (error) {
    ElMessage.error('获取部署列表失败')
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

async function handleStop(deployment: DeploymentItem) {
  try {
    await api.post(`/deploy/deployments/${deployment.id}/stop`)
    ElMessage.success('已暂停')
    fetchDeployments()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

async function handleStart(deployment: DeploymentItem) {
  try {
    const response = await api.post(`/deploy/deployments/${deployment.id}/start`)
    ElMessage.success('已启动')
    fetchDeployments()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

function handleVisit(deployment: DeploymentItem) {
  if (deployment.deployed_url) {
    window.open(deployment.deployed_url, '_blank')
  }
}

async function handleDelete(deployment: DeploymentItem) {
  try {
    await ElMessageBox.confirm(`确定要删除部署"${deployment.app_name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.delete(`/deploy/deployments/${deployment.id}`)
    ElMessage.success('删除成功')
    fetchDeployments()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(() => {
  fetchDeployments()
})
</script>

<style scoped>
.deployments-container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #f8fafc;
  margin-bottom: 8px;
}

.header p {
  color: #94a3b8;
}

.deployments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.deployment-card {
  background: #1e293b;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #334155;
  transition: all 0.3s;
}

.deployment-card.stopped {
  opacity: 0.7;
  border-color: #475569;
}

.deployment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.app-name {
  font-size: 18px;
  font-weight: 600;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-dot.running {
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.status-dot.stopped {
  background: #ef4444;
}

.deployment-url {
  margin-bottom: 12px;
}

.url-label {
  color: #94a3b8;
  font-size: 14px;
}

.url-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
}

.url-link:hover {
  text-decoration: underline;
}

.deployment-meta {
  display: flex;
  gap: 20px;
  color: #64748b;
  font-size: 13px;
  margin-bottom: 15px;
}

.deployment-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
</style>