<template>
  <div class="dashboard-container">
    <header class="header">
      <div>
        <h1 class="title">Explore!</h1>
        <p class="subtitle">Your Quiz Performances</p>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import api from '@/axios/axios'
import { useRouter } from 'vue-router'
const scores = ref([])
const loading = ref(true)

const router = useRouter()

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
