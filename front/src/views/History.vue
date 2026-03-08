<template>
  <div class="history-container">
    <div class="header">
      <h1>历史记录</h1>
      <p>查看您生成的所有代码历史</p>
    </div>

    <el-card>
      <el-table :data="historyList" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="描述" min-width="300">
          <template #default="{ row }">
            <div class="prompt-cell">{{ row.prompt }}</div>
          </template>
        </el-table-column>
        <el-table-column label="生成时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button @click="handleView(row)" text type="primary">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button @click="handleCopy(row)" text>
              <el-icon><DocumentCopy /></el-icon>
              复制
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- View Dialog -->
    <el-dialog v-model="viewVisible" title="查看代码" width="80%">
      <div class="dialog-content">
        <div class="prompt-section">
          <h4>描述：</h4>
          <p>{{ currentHistory?.prompt }}</p>
        </div>
        <pre class="code-section"><code>{{ currentHistory?.generated_code }}</code></pre>
      </div>
      <template #footer>
        <el-button @click="handleCopy(currentHistory!)">
          <el-icon><DocumentCopy /></el-icon>
          复制代码
        </el-button>
        <el-button type="primary" @click="handleRepublish(currentHistory!)">
          <el-icon><Upload /></el-icon>
          发布应用
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

interface HistoryItem {
  id: number
  prompt: string
  generated_code: string
  created_at: string
}

const historyList = ref<HistoryItem[]>([])
const loading = ref(false)
const viewVisible = ref(false)
const currentHistory = ref<HistoryItem | null>(null)

async function fetchHistory() {
  loading.value = true
  try {
    const response = await api.get('/code/history')
    historyList.value = response.data
  } catch (error) {
    ElMessage.error('获取历史记录失败')
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

function handleView(row: HistoryItem) {
  currentHistory.value = row
  viewVisible.value = true
}

function handleCopy(row: HistoryItem) {
  navigator.clipboard.writeText(row.generated_code)
  ElMessage.success('已复制到剪贴板')
}

function handleRepublish(row: HistoryItem) {
  viewVisible.value = false
  // Navigate to generate with the code (store in localStorage for simplicity)
  localStorage.setItem('republish_code', row.generated_code)
  localStorage.setItem('republish_prompt', row.prompt)
  // This would require additional implementation to pass data to Generate component
  ElMessage.info('请在代码生成页面重新发布')
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.history-container {
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

.prompt-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dialog-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.prompt-section h4 {
  color: #f8fafc;
  margin-bottom: 10px;
}

.prompt-section p {
  color: #94a3b8;
}

.code-section {
  background: #0f172a;
  padding: 20px;
  border-radius: 10px;
  overflow: auto;
  max-height: 400px;
  font-family: 'Consolas', monospace;
  font-size: 14px;
}

.code-section code {
  color: #e2e8f0;
  white-space: pre-wrap;
}
</style>
