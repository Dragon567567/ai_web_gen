<template>
  <div class="generate-container">
    <div class="header">
      <div class="header-left">
        <h1>代码生成</h1>
        <p>使用AI生成Web页面代码</p>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleSessionCommand">
          <el-button type="primary">
            <el-icon><FolderOpened /></el-icon>
            {{ currentSessionId ? '会话: ' + currentSessionTitle : '选择会话' }}
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="new">
                <el-icon><Plus /></el-icon>
                新建会话
              </el-dropdown-item>
              <el-dropdown-item v-for="session in sessions" :key="session.id" :command="session.id">
                {{ session.title }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div class="generate-content">
      <!-- 左侧聊天窗口 -->
      <div class="chat-section">
        <el-card class="chat-card">
          <!-- 聊天消息区域 -->
          <div class="chat-messages" ref="chatMessagesRef">
            <!-- 空状态 - 提示语 -->
            <div v-if="messages.length === 0" class="empty-chat">
              <div class="ai-avatar">
                <el-icon :size="40"><MagicStick /></el-icon>
              </div>
              <div class="welcome-text">
                <h3>你好，我是AI代码生成助手</h3>
                <p>描述你想要生成的页面，AI将为你创建完整的Web项目代码</p>
              </div>

              <!-- 快速提示 -->
              <div class="quick-prompts">
                <div class="prompt-label">试试这样描述：</div>
                <div class="prompt-tags">
                  <el-tag
                    v-for="prompt in quickPrompts"
                    :key="prompt"
                    class="prompt-tag"
                    @click="handleQuickPrompt(prompt)"
                  >
                    {{ prompt }}
                  </el-tag>
                </div>
              </div>
            </div>

            <!-- 消息列表 -->
            <div v-else>
              <div
                v-for="(msg, index) in messages"
                :key="index"
                :class="['message', msg.role]"
              >
                <div class="message-avatar">
                  <el-icon v-if="msg.role === 'user'"><User /></el-icon>
                  <el-icon v-else><MagicStick /></el-icon>
                </div>
                <div class="message-content">
                  <div v-if="msg.role === 'user'" class="user-text">{{ msg.content }}</div>
                  <div v-else-if="msg.role === 'assistant' && msg.isCode" class="code-result-info">
                    <el-icon><Document /></el-icon>
                    <span>已生成 {{ msg.files?.length || 0 }} 个文件</span>
                    <span class="view-hint">点击右侧查看</span>
                  </div>
                  <div v-else class="assistant-text">{{ msg.content }}</div>
                </div>
              </div>

              <!-- 加载状态 -->
              <div v-if="loading" class="message assistant loading">
                <div class="message-avatar loading-avatar">
                  <el-icon class="avatar-icon"><MagicStick /></el-icon>
                </div>
                <div class="message-content">
                  <div class="loading-content">
                    <!-- 动态标题 -->
                    <div class="loading-title">
                      <span class="loading-dot"></span>
                      <span class="loading-dot"></span>
                      <span class="loading-dot"></span>
                      <span>AI 正在工作中</span>
                    </div>
                    <!-- 进度步骤 -->
                    <div class="progress-steps">
                      <div
                        v-for="(step, index) in progressSteps"
                        :key="index"
                        :class="['progress-step', { active: step.active, completed: step.completed }]"
                      >
                        <div class="step-icon">
                          <el-icon v-if="step.completed"><Check /></el-icon>
                          <el-icon v-else-if="step.active" class="spinning"><Loading /></el-icon>
                          <span v-else>{{ index + 1 }}</span>
                        </div>
                        <span class="step-text">{{ step.text }}</span>
                      </div>
                    </div>
                    <!-- 进度条 -->
                    <div class="progress-bar-container">
                      <div class="progress-bar" :style="{ width: progress + '%' }">
                        <div class="progress-shine"></div>
                      </div>
                    </div>
                    <span class="loading-text">{{ currentProgressMessage }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="chat-input-area">
            <div class="input-wrapper">
              <el-input
                v-model="prompt"
                type="textarea"
                :rows="3"
                placeholder="描述你想要生成的页面，例如：创建一个登录页面..."
                :disabled="loading"
                resize="none"
                @keydown.enter.ctrl="handleGenerate"
              />
              <el-button
                type="primary"
                :loading="loading"
                @click="handleGenerate"
                class="send-btn"
                :disabled="!prompt.trim()"
              >
                <el-icon v-if="!loading"><Promotion /></el-icon>
                <span v-if="!loading">生成</span>
              </el-button>
            </div>
            <div class="input-hint">
              按 Ctrl + Enter 发送
            </div>
          </div>
        </el-card>
      </div>

      <!-- 右侧文件窗口 -->
      <div class="file-section">
        <el-card v-if="files.length > 0" class="file-card">
          <template #header>
            <div class="card-header">
              <span>生成的文件</span>
              <div class="header-actions">
                <el-button @click="handleCopy" text>
                  <el-icon><DocumentCopy /></el-icon>
                  复制
                </el-button>
                <el-button type="primary" @click="handlePreview">
                  <el-icon><View /></el-icon>
                  预览
                </el-button>
                <el-button type="warning" @click="handleDeploy">
                  <el-icon><Promotion /></el-icon>
                  Docker部署
                </el-button>
              </div>
            </div>
          </template>

          <!-- 文件列表 -->
          <div class="file-list">
            <!-- 前端文件 -->
            <template v-if="frontendFiles.length > 0">
              <div class="file-group-header">
                <el-icon><Monitor /></el-icon>
                <span>前端 ({{ frontendFiles.length }})</span>
              </div>
              <div
                v-for="file in frontendFiles"
                :key="file.filename"
                :class="['file-item', { active: currentFile.filename === file.filename }]"
                @click="currentFile = file"
              >
                <el-icon><Document /></el-icon>
                <span class="filename">{{ file.filename }}</span>
              </div>
            </template>

            <!-- 后端文件 -->
            <template v-if="backendFiles.length > 0">
              <div class="file-group-header">
                <el-icon><Cpu /></el-icon>
                <span>后端 ({{ backendFiles.length }})</span>
              </div>
              <div
                v-for="file in backendFiles"
                :key="file.filename"
                :class="['file-item', { active: currentFile.filename === file.filename }]"
                @click="currentFile = file"
              >
                <el-icon><Document /></el-icon>
                <span class="filename">{{ file.filename }}</span>
              </div>
            </template>
          </div>

          <!-- 代码预览/编辑 -->
          <div class="code-header">
            <span class="current-file">{{ currentFile.filename }}</span>
            <div class="code-actions">
              <el-button v-if="!isEditing" type="primary" text @click="startEdit">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <template v-else>
                <el-button type="success" text @click="saveEdit">
                  <el-icon><Check /></el-icon>
                  保存
                </el-button>
                <el-button type="info" text @click="cancelEdit">
                  <el-icon><Close /></el-icon>
                  取消
                </el-button>
              </template>
            </div>
          </div>
          <!-- 编辑模式 -->
          <textarea
            v-if="isEditing"
            v-model="editingContent"
            class="code-editor"
            spellcheck="false"
          ></textarea>
          <!-- 查看模式 -->
          <pre v-else class="code-preview"><code>{{ currentFile.content }}</code></pre>
        </el-card>

        <el-card v-else class="empty-card">
          <div class="empty-state">
            <el-icon :size="60"><Folder /></el-icon>
            <p>暂无生成文件</p>
            <span>在左侧描述你想要生成的页面，AI将为你生成代码</span>
          </div>
        </el-card>
      </div>
    </div>

    <!-- Preview Dialog -->
    <el-dialog
      v-model="previewVisible"
      title="预览"
      width="80%"
      :before-close="handleClosePreview"
    >
      <iframe
        v-if="previewVisible"
        :srcdoc="currentFile.content"
        class="preview-iframe"
        sandbox="allow-scripts"
      ></iframe>
    </el-dialog>

    <!-- Publish Dialog -->
    <el-dialog
      v-model="publishVisible"
      title="发布应用"
      width="500px"
    >
      <el-form :model="publishForm" label-width="80px">
        <el-form-item label="应用名称">
          <el-input v-model="publishForm.name" placeholder="请输入应用名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="publishForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入应用描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="publishVisible = false">取消</el-button>
        <el-button type="primary" :loading="publishLoading" @click="handlePublishSubmit">
          发布
        </el-button>
      </template>
    </el-dialog>

    <!-- Deploy Dialog -->
    <el-dialog
      v-model="deployVisible"
      title="Docker 部署"
      width="600px"
      :close-on-click-modal="!deployLoading"
    >
      <el-form :model="deployForm" label-width="80px">
        <el-form-item label="应用名称">
          <el-input v-model="deployForm.name" placeholder="请输入应用名称" :disabled="deployLoading" />
        </el-form-item>
        <!-- 部署日志 -->
        <el-form-item label="部署日志" v-if="deployLogs.length > 0">
          <div class="deploy-logs">
            <div v-for="(log, index) in deployLogs" :key="index" :class="['log-item', log.type]">
              <span class="log-icon" v-if="log.type === 'error'">✗</span>
              <span class="log-icon" v-else-if="log.type === 'success'">✓</span>
              <span class="log-icon" v-else>›</span>
              <span>{{ log.message }}</span>
            </div>
          </div>
        </el-form-item>
        <!-- 部署成功结果 -->
        <el-alert
          v-if="deployResult?.url"
          title="部署成功！"
          type="success"
          :description="'访问地址: ' + deployResult.url"
          show-icon
          :closable="false"
          style="margin-top: 15px;"
        />
      </el-form>
      <template #footer>
        <el-button @click="handleCloseDeploy" :disabled="deployLoading">关闭</el-button>
        <el-button type="warning" :loading="deployLoading" @click="handleDeploySubmit" v-if="!deployResult?.url">
          开始部署
        </el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, watch, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

interface CodeFile {
  filename: string
  content: string
  folder: string
}

// 计算属性：分组文件
const frontendFiles = computed(() => files.value.filter(f => f.folder === 'frontend'))
const backendFiles = computed(() => files.value.filter(f => f.folder === 'backend'))

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  isCode?: boolean
  files?: CodeFile[]
}

const router = useRouter()

// 会话管理
const sessions = ref<any[]>([])
const currentSessionId = ref<number | null>(null)
const currentSessionTitle = ref('新会话')

async function fetchSessions() {
  try {
    const response = await api.get('/session/sessions')
    sessions.value = response.data || []
  } catch (error) {
    console.error('获取会话列表失败', error)
  }
}

async function handleSessionCommand(command: number | string) {
  if (command === 'new') {
    // 创建新会话
    try {
      const response = await api.post('/session/sessions', {
        title: '新会话'
      })
      currentSessionId.value = response.data.id
      currentSessionTitle.value = response.data.title
      messages.value = []
      files.value = []
      generatedCode.value = ''
      await fetchSessions()
    } catch (error) {
      ElMessage.error('创建会话失败')
    }
  } else {
    // 加载会话
    await loadSession(command as number)
  }
}

async function loadSession(sessionId: number) {
  try {
    const response = await api.get(`/session/sessions/${sessionId}`)
    currentSessionId.value = sessionId
    currentSessionTitle.value = response.data.title

    // 转换消息格式，确保 files 是数组
    messages.value = response.data.messages.map((msg: any) => ({
      role: msg.role,
      content: msg.content,
      isCode: msg.files && Array.isArray(msg.files) && msg.files.length > 0,
      files: msg.files && Array.isArray(msg.files) ? msg.files : []
    }))

    // 如果有文件，更新文件列表
    const assistantMsgs = messages.value.filter((m: any) => m.role === 'assistant' && m.files && m.files.length > 0)
    if (assistantMsgs.length > 0) {
      const lastAssistantMsg = assistantMsgs[assistantMsgs.length - 1]
      files.value = lastAssistantMsg.files || []
      generatedCode.value = JSON.stringify(files.value)
      if (files.value.length > 0) {
        currentFile.value = files.value[0]
      }
    } else {
      files.value = []
      generatedCode.value = ''
    }
  } catch (error) {
    console.error('加载会话失败:', error)
    ElMessage.error('加载会话失败')
  }
}

async function saveMessage(role: string, content: string, isCode: boolean = false, msgFiles: CodeFile[] = []) {
  if (!currentSessionId.value) return

  try {
    await api.post(`/session/sessions/${currentSessionId.value}/messages`, {
      role,
      content,
      files: msgFiles
    })
  } catch (error) {
    console.error('保存消息失败', error)
  }
}

// 快速提示语
const quickPrompts = [
  '创建一个登录页面',
  '生成一个个人简历页面',
  '制作一个产品展示网站',
  '开发一个待办事项应用',
  '创建一个天气预报页面'
]

const chatMessagesRef = ref<HTMLElement>()
const prompt = ref('')
const loading = ref(false)
const generatedCode = ref('')
const files = ref<CodeFile[]>([])
const currentFile = ref<CodeFile>({ filename: '', content: '' })
const messages = ref<ChatMessage[]>([])
const previewVisible = ref(false)
const publishVisible = ref(false)
const publishLoading = ref(false)

// 编辑相关
const isEditing = ref(false)
const editingContent = ref('')
const originalContent = ref('')

function startEdit() {
  originalContent.value = currentFile.value.content
  editingContent.value = currentFile.value.content
  isEditing.value = true
}

function saveEdit() {
  currentFile.value.content = editingContent.value
  // 更新 files 数组中的内容
  const fileIndex = files.value.findIndex(f => f.filename === currentFile.value.filename)
  if (fileIndex !== -1) {
    files.value[fileIndex].content = currentFile.value.content
  }
  // 更新 generatedCode
  generatedCode.value = JSON.stringify(files.value)
  isEditing.value = false
  ElMessage.success('代码已保存')
}

function cancelEdit() {
  editingContent.value = originalContent.value
  isEditing.value = false
}

const publishForm = reactive({
  name: '',
  description: ''
})

const deployVisible = ref(false)
const deployLoading = ref(false)
const deployResult = ref<any>(null)
const deployLogs = ref<{message: string, type: string}[]>([])
const deployForm = reactive({
  name: ''
})

// 进度相关
const progress = ref(0)
const currentProgressMessage = ref('')
const progressSteps = ref([
  { text: '解析需求', active: false, completed: false },
  { text: 'AI 生成代码', active: false, completed: false },
  { text: 'AI 审查代码', active: false, completed: false },
  { text: '整理代码', active: false, completed: false },
])

function resetProgress() {
  progress.value = 0
  currentProgressMessage.value = ''
  progressSteps.value = [
    { text: '解析需求', active: false, completed: false },
    { text: 'AI 生成代码', active: false, completed: false },
    { text: 'AI 审查代码', active: false, completed: false },
    { text: '整理代码', active: false, completed: false },
  ]
}

function updateProgress(step: string, message: string, progressValue: number) {
  progress.value = progressValue
  currentProgressMessage.value = message

  // 更新步骤状态
  const stepMap: Record<string, number> = {
    'parsing': 0,
    'generating': 1,
    'reviewing': 2,
    'organizing': 3,
  }

  const stepIndex = stepMap[step]
  if (stepIndex !== undefined) {
    progressSteps.value.forEach((s, i) => {
      if (i < stepIndex) {
        s.completed = true
        s.active = false
      } else if (i === stepIndex) {
        s.active = true
        s.completed = false
      } else {
        s.active = false
        s.completed = false
      }
    })
  }
}

// 自动滚动到底部
watch(messages, async () => {
  await nextTick()
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}, { deep: true })

// 快速选择提示
function handleQuickPrompt(text: string) {
  prompt.value = text
}

// 页面加载时获取会话列表
onMounted(() => {
  fetchSessions()
})

// 发送消息
// 判断是否为修改请求的关键词
function isModifyRequest(text: string): boolean {
  const modifyKeywords = ['修改', '改一下', '改成', '改成', '修复', 'bug', '添加', '增加', '删除', '调整', '优化', '改进', '完善', '换个', '改颜色', '改样式', '改布局']
  return modifyKeywords.some(keyword => text.includes(keyword))
}

async function handleGenerate() {
  if (!prompt.value.trim()) {
    ElMessage.warning('请输入页面描述')
    return
  }

  const userMessage = prompt.value
  messages.value.push({ role: 'user', content: userMessage })
  prompt.value = ''
  loading.value = true
  resetProgress()

  // 如果没有会话，创建新会话
  if (!currentSessionId.value) {
    try {
      const response = await api.post('/session/sessions', {
        title: userMessage.substring(0, 30) + (userMessage.length > 30 ? '...' : '')
      })
      currentSessionId.value = response.data.id
      currentSessionTitle.value = response.data.title
      await fetchSessions()
    } catch (error) {
      console.error('创建会话失败', error)
    }
  }

  // 保存用户消息到会话
  await saveMessage('user', userMessage)

  // 判断是生成新代码还是修改现有代码
  const hasExistingCode = files.value.length > 0
  const shouldModify = hasExistingCode && isModifyRequest(userMessage)

  try {
    let response
    if (shouldModify) {
      // 修改现有代码
      updateProgress('modifying', '正在修改代码...', 0)

      // 调用修改 API
      const modifyResponse = await api.post('/code/modify', {
        original_code: generatedCode.value,
        feedback: userMessage
      })

      const modifiedFiles = modifyResponse.data || []

      // 更新文件列表
      files.value = modifiedFiles
      generatedCode.value = JSON.stringify(files.value)

      if (files.value.length > 0) {
        currentFile.value = files.value[0]
      }

      messages.value.push({
        role: 'assistant',
        content: `根据您的要求已修改代码：${userMessage}`,
        isCode: true,
        files: files.value
      })

      // 保存修改后的消息到会话
      await saveMessage('assistant', `根据您的要求已修改代码：${userMessage}`, true, files.value)

      loading.value = false
      ElMessage.success('代码修改成功')
      return
    }

    // 使用 SSE 流式获取进度（生成新代码）
    response = await fetch('/api/code/generate/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ prompt: userMessage })
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('无法读取响应')
    }

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      const lines = text.split('\n')

      for (const line of lines) {
        if (line.trim()) {
          try {
            const data = JSON.parse(line)

            if (data.step === 'error') {
              throw new Error(data.message)
            }

            updateProgress(data.step, data.message, data.progress)

            // 如果完成了，获取文件列表
            if (data.step === 'completed' && data.files) {
              files.value = data.files
              generatedCode.value = JSON.stringify(files.value)

              messages.value.push({
                role: 'assistant',
                content: '代码生成完成！',
                isCode: true,
                files: files.value
              })

              if (files.value.length > 0) {
                currentFile.value = files.value[0]
              }

              // 保存助手消息到会话
              await saveMessage('assistant', '代码生成完成！', true, files.value)

              ElMessage.success('代码生成成功')
            }
          } catch (e) {
            console.error('解析进度数据失败:', e)
          }
        }
      }
    }
  } catch (error: any) {
    messages.value.push({
      role: 'assistant',
      content: error.message || '生成失败，请重试'
    })
    ElMessage.error(error.message || '生成失败')
  } finally {
    loading.value = false
  }
}

function handleCopy() {
  if (currentFile.value.content) {
    navigator.clipboard.writeText(currentFile.value.content)
    ElMessage.success('已复制到剪贴板')
  }
}

function handlePreview() {
  previewVisible.value = true
}

function handleClosePreview() {
  previewVisible.value = false
}

function handlePublish() {
  if (!generatedCode.value) {
    ElMessage.warning('请先生成代码')
    return
  }
  publishForm.name = ''
  publishForm.description = ''
  publishVisible.value = true
}

async function handlePublishSubmit() {
  if (!publishForm.name.trim()) {
    ElMessage.warning('请输入应用名称')
    return
  }

  publishLoading.value = true
  try {
    await api.post('/apps', {
      name: publishForm.name,
      description: publishForm.description,
      code: generatedCode.value
    })
    ElMessage.success('发布成功')
    publishVisible.value = false
    router.push('/apps')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '发布失败')
  } finally {
    publishLoading.value = false
  }
}

function handleDeploy() {
  if (!generatedCode.value) {
    ElMessage.warning('请先生成代码')
    return
  }
  deployForm.name = ''
  deployResult.value = null
  deployLogs.value = []
  deployVisible.value = true
}

function handleCloseDeploy() {
  deployVisible.value = false
  deployLogs.value = []
}

async function handleDeploySubmit() {
  if (!deployForm.name.trim()) {
    ElMessage.warning('请输入应用名称')
    return
  }

  deployLoading.value = true
  deployLogs.value = []
  deployResult.value = null

  try {
    const response = await fetch('/api/deploy/deploy/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        name: deployForm.name,
        code: generatedCode.value
      })
    })

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('无法读取响应')
    }

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const text = decoder.decode(value)
      const lines = text.split('\n')

      for (const line of lines) {
        if (line.trim()) {
          try {
            const data = JSON.parse(line)

            if (data.status === 'log') {
              deployLogs.value.push({ message: data.message, type: 'info' })
            } else if (data.status === 'error') {
              deployLogs.value.push({ message: data.message, type: 'error' })
            } else if (data.status === 'completed') {
              deployResult.value = data
              ElMessage.success('部署成功！')
            }
          } catch (e) {
            console.error('解析日志失败:', e)
          }
        }
      }
    }
  } catch (error: any) {
    deployLogs.value.push({ message: error.message || '部署失败', type: 'error' })
    ElMessage.error(error.message || '部署失败')
  } finally {
    deployLoading.value = false
  }
}
</script>

<style scoped>
.generate-container {
  max-width: 1600px;
  margin: 0 auto;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.header {
  margin-bottom: 20px;
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  font-size: 28px;
  color: #f8fafc;
  margin-bottom: 8px;
}

.header-left p {
  color: #94a3b8;
}

.generate-content {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

/* 左侧聊天窗口 */
.chat-section {
  width: 40%;
  display: flex;
  flex-direction: column;
}

.chat-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  --el-card-padding: 20px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 15px;
  max-height: 450px;
  min-height: 300px;
  background: #111827;
  border-radius: 12px;
}

/* 空状态 - 欢迎界面 */
.empty-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 20px;
}

.empty-chat .ai-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 20px;
}

.empty-chat .welcome-text h3 {
  color: #f9fafb;
  font-size: 20px;
  margin-bottom: 10px;
}

.empty-chat .welcome-text p {
  color: #9ca3af;
  font-size: 14px;
  margin-bottom: 25px;
}

.quick-prompts {
  width: 100%;
}

.prompt-label {
  color: #6b7280;
  font-size: 12px;
  margin-bottom: 12px;
  text-align: left;
}

.prompt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.prompt-tag {
  cursor: pointer;
  transition: all 0.2s;
  background: #1f2937;
  color: #d1d5db;
  border-color: #374151;
}

.prompt-tag:hover {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* 消息样式 */
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #3b82f6;
  color: white;
}

.message.assistant .message-avatar {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.message-content {
  max-width: 75%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
}

.message.user .message-content {
  background: #3b82f6;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: #1f2937;
  color: #e5e7eb;
  border-bottom-left-radius: 4px;
}

.user-text {
  word-break: break-word;
}

.assistant-text {
  color: #d1d5db;
}

.code-result-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #10b981;
}

.view-hint {
  font-size: 12px;
  color: #6b7280;
  margin-left: 8px;
}

/* 加载状态 */
.message.loading .message-content {
  padding: 12px 16px;
}

.loading-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.loading-text {
  color: #9ca3af;
  font-size: 13px;
}

.loading-bar {
  width: 120px;
  height: 4px;
  background: #374151;
  border-radius: 2px;
  overflow: hidden;
}

.loading-progress {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  border-radius: 2px;
  animation: loading 1.5s ease-in-out infinite;
}

@keyframes loading {
  0% { width: 0%; margin-left: 0; }
  50% { width: 60%; margin-left: 20%; }
  100% { width: 0%; margin-left: 100%; }
}

/* 进度步骤 */
.progress-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #6b7280;
  font-size: 13px;
}

.progress-step.active {
  color: #3b82f6;
}

.progress-step.completed {
  color: #10b981;
}

/* 动态加载标题 */
.loading-title {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #3b82f6;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 15px;
}

.loading-dot {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  animation: dotPulse 1.4s infinite ease-in-out;
}

.loading-dot:nth-child(1) {
  animation-delay: 0s;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotPulse {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 头像旋转动画 */
.loading-avatar {
  animation: avatarPulse 2s ease-in-out infinite;
}

.avatar-icon {
  animation: iconRotate 1s linear infinite;
}

@keyframes avatarPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

@keyframes iconRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 旋转图标 */
.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 进度条闪光效果 */
.progress-bar {
  position: relative;
  overflow: hidden;
}

.progress-shine {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shine 2s ease-in-out infinite;
}

@keyframes shine {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.step-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #374151;
  font-size: 11px;
  color: #9ca3af;
}

.progress-step.active .step-icon {
  background: #3b82f6;
  color: white;
}

.progress-step.completed .step-icon {
  background: #10b981;
  color: white;
}

.step-text {
  flex: 1;
}

.progress-bar-container {
  width: 100%;
  height: 4px;
  background: #374151;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #3b82f6);
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* 输入区域 */
.chat-input-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-wrapper {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-wrapper :deep(.el-textarea) {
  flex: 1;
}

.input-wrapper :deep(.el-textarea__inner) {
  background: #1f2937;
  border-color: #374151;
  color: #f9fafb;
  border-radius: 12px;
}

.input-wrapper :deep(.el-textarea__inner:focus) {
  border-color: #3b82f6;
}

.send-btn {
  height: auto;
  padding: 10px 20px;
  border-radius: 12px;
}

.input-hint {
  font-size: 12px;
  color: #6b7280;
  text-align: right;
}

/* 右侧文件窗口 */
.file-section {
  width: 60%;
  display: flex;
  flex-direction: column;
}

.file-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  --el-card-padding: 16px;
}

.file-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #374151;
}

.file-group-header {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #9ca3af;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 8px;
  padding-left: 4px;
}

.file-group-header:first-child {
  margin-top: 0;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #1f2937;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #9ca3af;
  transition: all 0.2s;
}

.file-item:hover {
  background: #374151;
  color: #e5e7eb;
}

.file-item.active {
  background: #3b82f6;
  color: white;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.current-file {
  font-size: 14px;
  color: #9ca3af;
}

.code-actions {
  display: flex;
  gap: 8px;
}

.code-editor {
  flex: 1;
  background: #0f172a;
  color: #e2e8f0;
  padding: 20px;
  border-radius: 10px;
  font-family: 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.6;
  min-height: 300px;
  border: 2px solid #3b82f6;
  resize: vertical;
  outline: none;
}

.code-preview {
  flex: 1;
  background: #0f172a;
  padding: 20px;
  border-radius: 10px;
  overflow: auto;
  font-family: 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.6;
  min-height: 300px;
}

.code-preview code {
  color: #e2e8f0;
  white-space: pre-wrap;
  word-break: break-all;
}

.empty-card {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  text-align: center;
  color: #6b7280;
}

.empty-state p {
  margin: 15px 0 8px;
  font-size: 16px;
  color: #9ca3af;
}

.empty-state span {
  font-size: 14px;
}

.preview-iframe {
  width: 100%;
  height: 600px;
  border: none;
  border-radius: 10px;
  background: white;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* 部署日志 */
.deploy-logs {
  background: #1a1a2e;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
}

.log-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
  color: #9ca3af;
}

.log-item.error {
  color: #ef4444;
}

.log-item.success {
  color: #10b981;
}

.log-icon {
  flex-shrink: 0;
  width: 16px;
  text-align: center;
}
</style>
