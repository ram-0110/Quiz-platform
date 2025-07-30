<template>
  <div class="dashboard-container">
    <header class="header">
      <div class="header-content">
        <div>
          <h1 class="title">Explore!</h1>
          <p class="subtitle">Your Quiz Performances</p>
        </div>

        <button @click="downloadCSV" :disabled="downloadLoading" class="download-btn">
          <span v-if="downloadLoading" class="loading-spinner"></span>
          <svg
            v-else
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7,10 12,15 17,10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          {{ downloadLoading ? 'Downloading...' : 'Download CSV' }}
        </button>
      </div>
    </header>

    <div v-if="loading" class="loading-state">
      <p>Loading your scores...</p>
    </div>

    <div v-else-if="scores.length === 0" class="empty-state">
      <p>No scores found.</p>
      <p class="suggestion">Take some quizzes to see your performance here.</p>
    </div>

    <div v-else class="scores-container">
      <div
        v-for="score in scores"
        :key="score.score_id"
        class="score-card"
        @click="goToResult(score.quiz.quiz_id)"
        role="button"
        tabindex="0"
      >
        <h3 class="score-title">
          {{ score.subject.subject_name }} → {{ score.chapter.chapter_name }}
        </h3>
        <p class="quiz-meta">Quiz: {{ score.quiz.quiz_name }} ({{ score.quiz.date_of_quiz }})</p>
        <p class="score-value">
          Score: <strong>{{ score.total_score }}</strong>
        </p>
        <p class="timestamp">Taken on: {{ score.timestamp }}</p>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="downloadMessage" :class="['message', downloadMessage.type]">
      {{ downloadMessage.text }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import api from '@/axios/axios'
import { useRouter } from 'vue-router'

const scores = ref([])
const loading = ref(true)
const downloadLoading = ref(false)
const downloadMessage = ref(null)

const router = useRouter()
async function downloadCSV() {
  downloadLoading.value = true
  downloadMessage.value = null

  try {
    const response = await api.get('/download-user-data', {
      responseType: 'blob',
    })

    // Handle filename extraction more safely
    let filename = 'quiz_results.csv'
    if (response.headers['content-disposition']) {
      const contentDisposition = response.headers['content-disposition']
      const filenameMatch = contentDisposition.match(/filename\*?=["']?([^"';]+)["']?/)
      if (filenameMatch && filenameMatch[1]) {
        filename = decodeURIComponent(filenameMatch[1])
      } else {
        // Fallback: Extract filename without encoding
        const simpleMatch = contentDisposition.match(/filename=["']?([^"';]+)["']?/)
        if (simpleMatch && simpleMatch[1]) {
          filename = simpleMatch[1]
        }
      }
    }

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()

    // Clean up
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    downloadMessage.value = {
      text: 'Download started successfully!',
      type: 'success',
    }
  } catch (error) {
    console.error('Download error:', error)
    downloadMessage.value = {
      text: error.response?.data?.error || 'Failed to download data. Please try again.',
      type: 'error',
    }
  } finally {
    downloadLoading.value = false

    // Clear message after 3 seconds
    setTimeout(() => {
      downloadMessage.value = null
    }, 3000)
  }
}

function goToResult(quizId) {
  router.push(`/quiz/result/${quizId}`)
}
onMounted(async () => {
  try {
    const response = await api.get('/home')
    scores.value = response.data.scores || []
  } catch (error) {
    console.error('Error fetching scores:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.download-btn:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-1px);
}

.download-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: 500;
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.message.success {
  background-color: #10b981;
  color: white;
}

.message.error {
  background-color: #ef4444;
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.score-card {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #ffffff;
  padding: 1.25rem;
  cursor: pointer;
}

.score-card:hover {
  background-color: #f9f9f9;
}
.dashboard-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #000;
  background-color: #fff;
  max-width: 92vw;
  margin: 0 auto;
  padding: 1.5rem;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e2e2;
}

.title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
}

.subtitle {
  font-size: 0.875rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 150px;
  color: #757575;
  font-size: 0.95rem;
}

.empty-state {
  background-color: #fafafa;
  border: 1px solid #eeeeee;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  margin: 2rem 0;
}

.suggestion {
  color: #757575;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.scores-container {
  margin-top: 1rem;
  display: grid;
  gap: 1rem;
}

.score-card {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  background-color: #ffffff;
  padding: 1.25rem;
}

.score-title {
  font-size: 1rem;
  font-weight: 600;
  color: #212121;
  margin-bottom: 0.25rem;
}

.quiz-meta {
  font-size: 0.875rem;
  color: #555;
  margin-bottom: 0.25rem;
}

.score-value {
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.timestamp {
  font-size: 0.75rem;
  color: #888;
}
</style>
