<template>
  <div class="dashboard-container">
    <PageHeader title="Admin Dashboard" subtitle="Monitor user performance and system statistics" />

    <div class="summary-section">
      <div class="summary-card">
        <div class="summary-icon"></div>
        <div class="summary-content">
          <h3>Total Users</h3>
          <p class="summary-number">{{ allUsers.length }}</p>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"></div>
        <div class="summary-content">
          <h3>Inactive Users</h3>
          <p class="summary-number">{{ inactiveUsers.length }}</p>
        </div>
      </div>
      <div class="summary-card">
        <div class="summary-icon"></div>
        <div class="summary-content">
          <h3>Subjects</h3>
          <p class="summary-number">{{ averageScores.length }}</p>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Top Scorers by Subject</h2>
      <div class="top-scorers-grid">
        <div v-for="subject in topScorers" :key="subject.subject" class="subject-card">
          <h3 class="subject-name">{{ subject.subject }}</h3>
          <div class="scorers-list">
            <div
              v-for="(scorer, index) in subject.top_scorers"
              :key="scorer.username"
              class="scorer-item"
            >
              <div class="scorer-rank">{{ index + 1 }}</div>
              <div class="scorer-info">
                <span class="scorer-name">{{ scorer.username }}</span>
                <span class="scorer-score">{{ scorer.total_score }} pts</span>
              </div>
            </div>
            <div v-if="subject.top_scorers.length === 0" class="no-data">No scores yet</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Average Scores by Subject</h2>
      <div class="average-scores-grid">
        <div v-for="subject in averageScores" :key="subject.subject" class="average-card">
          <h3>{{ subject.subject }}</h3>
          <div class="average-score">
            <span class="score-value">{{ subject.average_score }}%</span>
            <div class="score-bar">
              <div
                class="score-fill"
                :style="{ width: `${Math.min(subject.average_score, 100)}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Recent Quiz Participation</h2>
      <div class="participation-table">
        <div class="table-header">
          <div>Quiz Name</div>
          <div>Date</div>
          <div>Attempts</div>
        </div>
        <div v-for="quiz in quizParticipation" :key="quiz.quiz_name" class="table-row">
          <div class="quiz-name">{{ quiz.quiz_name }}</div>
          <div class="quiz-date">{{ formatDate(quiz.date) }}</div>
          <div class="quiz-attempts">
            <span class="attempts-badge">{{ quiz.attempts }}</span>
          </div>
        </div>
        <div v-if="quizParticipation.length === 0" class="no-data">No quiz data available</div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">User Progress</h2>
      <div class="user-progress-section">
        <div class="user-selector">
          <label for="user-select" class="filter-label">Select User</label>
          <select
            id="user-select"
            v-model="selectedUserId"
            class="filter-select"
            @change="fetchUserProgress"
          >
            <option value="" disabled>Choose a user</option>
            <option v-for="user in allUsers" :key="user.id" :value="user.id">
              {{ user.username }} ({{ user.email }})
            </option>
          </select>
        </div>

        <div v-if="userProgress.length > 0" class="progress-display">
          <div v-for="subject in userProgress" :key="subject.subject" class="subject-progress">
            <h3>{{ subject.subject }}</h3>
            <div class="chapters-progress">
              <div
                v-for="chapter in subject.chapters"
                :key="chapter.chapter"
                class="chapter-progress"
              >
                <div class="chapter-header">
                  <span class="chapter-name">{{ chapter.chapter }}</span>
                  <span class="chapter-stats">
                    {{ chapter.completed_quizzes }}/{{ chapter.total_quizzes }} ({{
                      chapter.progress_percent
                    }}%)
                  </span>
                </div>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: `${chapter.progress_percent}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="selectedUserId && userProgress.length === 0" class="no-data">
          No progress data for selected user
        </div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">Inactive Users (30+ days)</h2>
      <div class="inactive-users-grid">
        <div v-for="user in inactiveUsers" :key="user.username" class="inactive-user-card">
          <div class="user-info">
            <h4>{{ user.username }}</h4>
            <p>{{ user.email }}</p>
          </div>
          <div class="last-seen">Last seen: {{ formatDate(user.last_seen) }}</div>
        </div>
        <div v-if="inactiveUsers.length === 0" class="no-data">No inactive users found</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/axios/axios'
import PageHeader from '@/components/PageHeader.vue'

// Reactive data
const allUsers = ref([])
const topScorers = ref([])
const averageScores = ref([])
const quizParticipation = ref([])
const inactiveUsers = ref([])
const userProgress = ref([])
const selectedUserId = ref('')

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const fetchAllUsers = async () => {
  try {
    const response = await api.get('/admin/users')
    allUsers.value = response.data
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

const fetchTopScorers = async () => {
  try {
    const response = await api.get('/admin/top-scorers')
    topScorers.value = response.data
  } catch (error) {
    console.error('Failed to fetch top scorers:', error)
  }
}

const fetchAverageScores = async () => {
  try {
    const response = await api.get('/admin/average-scores')
    averageScores.value = response.data
  } catch (error) {
    console.error('Failed to fetch average scores:', error)
  }
}

const fetchQuizParticipation = async () => {
  try {
    const response = await api.get('/admin/quiz-participation')
    quizParticipation.value = response.data
  } catch (error) {
    console.error('Failed to fetch quiz participation:', error)
  }
}

const fetchInactiveUsers = async () => {
  try {
    const response = await api.get('/admin/inactive-users')
    inactiveUsers.value = response.data
  } catch (error) {
    console.error('Failed to fetch inactive users:', error)
  }
}

const fetchUserProgress = async () => {
  if (!selectedUserId.value) return

  try {
    const response = await api.get(`/admin/user-progress/${selectedUserId.value}`)
    userProgress.value = response.data
  } catch (error) {
    console.error('Failed to fetch user progress:', error)
    userProgress.value = []
  }
}

onMounted(async () => {
  await Promise.all([
    fetchAllUsers(),
    fetchTopScorers(),
    fetchAverageScores(),
    fetchQuizParticipation(),
    fetchInactiveUsers(),
  ])
})
</script>

<style scoped>
.dashboard-container {
  font-family:
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    'Noto Sans',
    sans-serif;
  color: hsl(0 0% 3.9%);
  background-color: hsl(0 0% 100%);
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  line-height: 1.5;
}

.summary-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #2f2f2f 0%, #2f2f2f 100%);
  color: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.summary-content h3 {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 500;
  opacity: 0.9;
}

.summary-number {
  margin: 0.25rem 0 0 0;
  font-size: 2rem;
  font-weight: 700;
}

.section {
  margin: 3rem 0;
  padding: 2rem;
  background-color: hsl(0 0% 98%);
  border: 1px solid hsl(0 0% 89.8%);
  border-radius: 0.75rem;
}

.section-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: hsl(0 0% 3.9%);
}

.top-scorers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.subject-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid hsl(0 0% 89.8%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.subject-name {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: hsl(0 0% 3.9%);
}

.scorers-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.scorer-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background-color: hsl(0 0% 96.1%);
  border-radius: 0.375rem;
}

.scorer-rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: linear-gradient(135deg, #949494 0%, #000000 100%);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 0.875rem;
}

.scorer-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.scorer-name {
  font-weight: 500;
  color: hsl(0 0% 3.9%);
}

.scorer-score {
  font-size: 0.875rem;
  color: hsl(0 0% 45.1%);
}

.average-scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.average-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid hsl(0 0% 89.8%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.average-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.score-value {
  font-size: 2rem;
  font-weight: 700;
  color: hsl(0 0% 3.9%);
}

.score-bar {
  width: 100%;
  height: 0.5rem;
  background-color: hsl(0 0% 89.8%);
  border-radius: 0.25rem;
  margin-top: 0.5rem;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(135deg, #787878 0%, #000000 100%);
  transition: width 0.3s ease;
}

.participation-table {
  background: white;
  border-radius: 0.5rem;
  border: 1px solid hsl(0 0% 89.8%);
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background-color: hsl(0 0% 96.1%);
  font-weight: 600;
  color: hsl(0 0% 3.9%);
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid hsl(0 0% 89.8%);
  align-items: center;
}

.table-row:hover {
  background-color: hsl(0 0% 98%);
}

.quiz-name {
  font-weight: 500;
}

.attempts-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  height: 1.5rem;
  padding: 0 0.5rem;
  background: linear-gradient(135deg, #5c5c5c 0%, #5c5c5c 100%);
  color: white;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.user-selector {
  margin-bottom: 2rem;
}

.filter-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: hsl(0 0% 3.9%);
}

.filter-select {
  width: 100%;
  max-width: 400px;
  padding: 0.75rem;
  font-size: 0.875rem;
  color: hsl(0 0% 3.9%);
  background-color: white;
  border: 1px solid hsl(0 0% 89.8%);
  border-radius: 0.375rem;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: hsl(0 0% 3.9%);
  box-shadow: 0 0 0 2px hsl(0 0% 3.9% / 0.1);
}

.subject-progress {
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid hsl(0 0% 89.8%);
}

.subject-progress h3 {
  margin: 0 0 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.chapters-progress {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-progress {
  padding: 1rem;
  background-color: hsl(0 0% 98%);
  border-radius: 0.375rem;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.chapter-name {
  font-weight: 500;
}

.chapter-stats {
  font-size: 0.875rem;
  color: hsl(0 0% 45.1%);
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: hsl(0 0% 89.8%);
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #454545 0%, #6c6c6c 100%);
  transition: width 0.3s ease;
}

.inactive-users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.inactive-user-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid hsl(0 0% 89.8%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.user-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.user-info p {
  margin: 0 0 1rem 0;
  color: hsl(0 0% 45.1%);
}

.last-seen {
  font-size: 0.875rem;
  color: hsl(0 0% 45.1%);
  padding: 0.5rem;
  background-color: hsl(0 0% 96.1%);
  border-radius: 0.25rem;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: hsl(0 0% 45.1%);
  font-style: italic;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .section {
    padding: 1.5rem;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .chapter-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>
