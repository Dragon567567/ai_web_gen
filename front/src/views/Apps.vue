<template>
  <div class="apps-container">
    <div class="header">
      <h1>我的应用</h1>
      <p>管理您已发布的所有Web应用</p>
    </div>

    <div class="apps-grid" v-loading="loading">
      <el-empty v-if="!loading && appsList.length === 0" description="暂无应用" />
      <div
        v-for="app in appsList"
        :key="app.id"
        class="app-card"
      >
        <div class="app-preview">
          <iframe :srcdoc="app.code" sandbox="allow-scripts"></iframe>
        </div>
        <div class="app-info">
          <h3>{{ app.name }}</h3>
          <p>{{ app.description || '暂无描述' }}</p>
          <div class="app-meta">
            <span>创建于：{{ formatDate(app.created_at) }}</span>
          </div>
          <div class="app-actions">
            <el-button type="primary" size="small" @click="handleView(app)">
              <el-icon><View /></el-icon>
              预览
            </el-button>
            <el-button size="small" @click="handleEdit(app)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(app)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Preview Dialog -->
    <el-dialog
      v-model="previewVisible"
      title="预览应用"
      width="80%"
    >
      <iframe
        v-if="previewVisible"
        :srcdoc="currentApp?.code"
        class="preview-iframe"
        sandbox="allow-scripts"
      ></iframe>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

interface AppItem {
  id: number
  name: string
  description: string
  code: string
  is_published: number
  created_at: string
  updated_at: string
}

const appsList = ref<AppItem[]>([])
const loading = ref(false)
const previewVisible = ref(false)
const currentApp = ref<AppItem | null>(null)

async function fetchApps() {
  loading.value = true
  try {
    const response = await api.get('/apps')
    appsList.value = response.data.apps
  } catch (error) {
    ElMessage.error('获取应用列表失败')
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

function handleView(app: AppItem) {
  currentApp.value = app
  previewVisible.value = true
}

function handleEdit(app: AppItem) {
  // Navigate to generate with existing code
  ElMessage.info('编辑功能开发中')
}

async function handleDelete(app: AppItem) {
  try {
    await ElMessageBox.confirm(`确定要删除应用"${app.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.delete(`/apps/${app.id}`)
    ElMessage.success('删除成功')
    fetchApps()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(() => {
  fetchApps()
})
</script>

<style scoped>
.apps-container {
  max-width: 1400px;
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

.apps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.app-card {
  background: #1e293b;
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid #334155;
  transition: transform 0.3s, box-shadow 0.3s;
}

.app-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.app-preview {
  height: 200px;
  background: white;
  border-bottom: 1px solid #334155;
}

.app-preview iframe {
  width: 100%;
  height: 100%;
  border: none;
  transform: scale(0.5);
  transform-origin: top left;
  width: 200%;
  height: 200%;
}

.app-info {
  padding: 20px;
}

.app-info h3 {
  color: #f8fafc;
  font-size: 18px;
  margin-bottom: 8px;
}

.app-info p {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-meta {
  color: #64748b;
  font-size: 12px;
  margin-bottom: 15px;
}

.app-actions {
  display: flex;
  gap: 10px;
}

.preview-iframe {
  width: 100%;
  height: 600px;
  border: none;
  border-radius: 10px;
  background: white;
}
</style>
