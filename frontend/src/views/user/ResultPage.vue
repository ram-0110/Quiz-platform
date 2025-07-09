<template>
  <div class="min-h-screen bg-white flex items-center justify-center p-6">
    <div class="w-full max-w-md text-center">
      <!-- Loading -->
      <div v-if="loading" class="py-12">
        <div
          class="w-10 h-10 mx-auto border-4 border-gray-300 border-t-black rounded-full animate-spin"
        ></div>
        <p class="text-gray-600 mt-6">Loading your results...</p>
      </div>

      <!-- Error -->
      <div v-else-if="!result" class="p-8 border border-red-200 rounded-md bg-red-50">
        <p class="text-red-600 font-semibold mb-4">Failed to load results.</p>
        <button
          @click="fetchResult"
          class="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 transition-colors"
        >
          Try Again
        </button>
      </div>

      <div v-else class="dashboard-container">
        <PageHeader title="Welcome back Admin!" subtitle="Manage your subjects and quizzes" />

        <div class="subDir">
          <h2 class="score-display">{{ result.total_score }}</h2>
          <p class="score-label">Final Score</p>

          <div class="result-details">
            <div class="detail-item">
              <span class="detail-label">Quiz ID:</span>
              <span class="detail-value">{{ result.quiz_name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Remarks:</span>
              <span class="detail-value">{{ result.remarks || 'No remarks' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Submitted:</span>
              <span class="detail-value">{{ formatDate(result.timestamp) }}</span>
            </div>
          </div>

          <RouterLink to="/dashboard" class="back-button"> Back to Dashboard </RouterLink>
        </div>
      </div>

      <!-- Result -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/axios/axios'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const result = ref(null)
const loading = ref(true)

const fetchResult = async () => {
  loading.value = true
  try {
    const quizId = route.params.quizId
    const res = await api.get(`/quiz/result/${quizId}`)
    result.value = res.data
  } catch (err) {
    console.error('Fetch failed:', err)
    result.value = null
  } finally {
    loading.value = false
  }
}

const formatDate = (timestamp) =>
  new Date(timestamp).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

onMounted(fetchResult)
</script>

<style scoped>
.subDir {
  border-bottom: 1px solid #e2e2e2;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
}

/* Base styles */
.dashboard-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #000;
  background-color: #fff;
  max-width: 70vw;
  margin: 0 auto;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  margin-top: 2rem;
}

/* Header styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
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
  margin: 0.5rem 0 0 0;
}

/* Score display */
.score-display {
  font-size: 3rem;
  font-weight: 700;
  color: #000;
  margin: 1.5rem 0 0.5rem 0;
  line-height: 1;
}

.score-label {
  font-size: 1rem;
  color: #666;
  margin: 0 0 2rem 0;
  font-weight: 500;
}

/* Result details */
.result-details {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e9ecef;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: #495057;
  font-size: 0.875rem;
}

.detail-value {
  color: #000;
  font-size: 0.875rem;
  text-align: right;
  max-width: 60%;
  word-wrap: break-word;
}

/* Back button */
.back-button {
  display: inline-block;
  background-color: #000;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.back-button:hover {
  background-color: #333;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .dashboard-container {
    padding: 1.5rem;
  }

  .score-display {
    font-size: 2.5rem;
  }

  .result-details {
    padding: 1rem;
  }

  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .detail-value {
    max-width: 100%;
    text-align: left;
  }
}
</style>
