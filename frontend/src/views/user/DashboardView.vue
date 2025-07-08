<!-- dashboardView.vue -->
<script setup>
import subject_quiz_scroll from '@/components/subject_quiz_scroll.vue'
import api from '@/axios/axios'
import { onMounted, ref } from 'vue'
const name = ref('')
const subjects = ref([])
const isLoading = ref(true)
onMounted(async () => {
  try {
    const response = await api.get('/dashboard')
    name.value = response.data.username
    subjects.value = response.data.subjects
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="dashboard-view dashboard-container">
    <header class="header">
      <div>
        <h1 class="title">Welcome back, {{ name }}!</h1>
        <p class="subtitle">Continue your learning journey</p>
      </div>
    </header>

    <div v-if="isLoading" class="loading-state">
      <p>Loading your subjects...</p>
    </div>

    <div v-else-if="subjects.length === 0" class="empty-state">
      <p>You're not enrolled in any subjects yet.</p>
      <p class="suggestion">Explore our catalog to find subjects that interest you.</p>
    </div>

    <div v-else class="subjects-container">
      <div v-for="subject in subjects" :key="subject.id" class="subject-card">
        <subject_quiz_scroll :subject="subject" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #000;
  background-color: #fff;
  max-width: 92vw;
  margin: 0 auto;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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

.welcome-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-top: 1rem;
  line-height: 1.2;
  color: #212121;
}
.user-name {
  position: relative;
  display: inline-block;
}
.user-name::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #000;
  opacity: 0.1;
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
  height: 200px;
  color: #757575;
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
.subjects-container {
  margin-top: 1rem;
}
</style>
