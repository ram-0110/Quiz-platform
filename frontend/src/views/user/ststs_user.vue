<template>
  <div class="dashboard-container">
    <PageHeader title="Statistics!" subtitle="Look at your performance" />

    <!-- Filters -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="subject" class="filter-label">Subject</label>
        <select id="subject" v-model="active_subject" class="filter-select">
          <option value="" disabled selected>Select Subject</option>
          <option
            v-for="subject in subjectRef"
            :key="subject.subject_id"
            :value="subject.subject_id"
          >
            {{ subject.subject_name }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label for="chapter" class="filter-label">Chapter</label>
        <select id="chapter" v-model="active_chapter" class="filter-select">
          <option value="" disabled selected>Select Chapter</option>
          <option
            v-for="chapter in filteredChapters"
            :key="chapter.chapter_id"
            :value="chapter.chapter_id"
          >
            {{ chapter.chapter_name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-section">
      <div class="chart-container" v-if="subjectRef.length">
        <RadarChart :subjects="subjectRef" />
      </div>
      <div class="chart-container">
        <div class="chart-container" v-if="selectedSubject">
          <SubjectProgress
            :label="`Subject: ${selectedSubject.subject_name}`"
            :attempted="selectedSubject.attempted_quizzes"
            :total="selectedSubject.total_quizzes"
          />
        </div>

        <div class="chart-container" v-if="selectedChapter">
          <VerticalBar
            :label="`Chapter: ${selectedChapter.chapter_name}`"
            :scored="selectedChapter.attempted_quizzes"
            :total="selectedChapter.total_quizzes"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import api from '@/axios/axios'

import PageHeader from '@/components/PageHeader.vue'
import RadarChart from '@/components/RadarChart.vue'
import VerticalBar from '@/components/VerticalBar.vue'
import SubjectProgress from '@/components/SubjectProgress.vue'

const subjectRef = ref([])
const chapterRef = ref([])
const quizRef = ref([])

const active_subject = ref(null)
const active_chapter = ref(null)

watch(active_subject, () => {
  active_chapter.value = null
})

const filteredChapters = computed(() => {
  if (!active_subject.value) return []
  return chapterRef.value.filter((ch) => ch.subject_id === active_subject.value)
})

const selectedSubject = computed(() =>
  subjectRef.value.find((s) => s.subject_id === active_subject.value),
)

const selectedChapter = computed(() =>
  chapterRef.value.find((c) => c.chapter_id === active_chapter.value),
)

onMounted(async () => {
  try {
    const res = await api.get(`/stats/static`)
    subjectRef.value = res.data.subject_wise
    chapterRef.value = res.data.chapter_wise
    quizRef.value = res.data.quiz_wise
    console.log('Stats response:', res.data)

    await nextTick()
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
})
</script>

<style scoped>
.charts-section {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2rem;
  justify-content: center;
}

.chart-container {
  flex: 1 1 400px;
  min-width: 300px;
  max-width: 500px;
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid hsl(0 0% 89.8%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

@media (max-width: 768px) {
  .charts-section {
    flex-direction: column;
    align-items: center;
  }
}

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
    sans-serif,
    'Apple Color Emoji',
    'Segoe UI Emoji',
    'Segoe UI Symbol',
    'Noto Color Emoji';
  color: hsl(0 0% 3.9%);
  background-color: hsl(0 0% 100%);
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  border: 1px solid hsl(0 0% 89.8%);
  border-radius: 0.5rem;
  line-height: 1.5;
}

.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background-color: hsl(0 0% 98%);
  border: 1px solid hsl(0 0% 89.8%);
  border-radius: 0.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 240px;
  flex: 1;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: hsl(0 0% 3.9%);
  line-height: 1.25rem;
}

.filter-select {
  display: flex;
  height: 2.5rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  color: hsl(0 0% 3.9%);
  background-color: hsl(0 0% 100%);
  border: 1px solid hsl(0 0% 89.8%);
  border-radius: 0.375rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23374151' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1rem 1rem;
  padding-right: 2.5rem;
}

.filter-select:hover {
  border-color: hsl(0 0% 70%);
}

.filter-select:focus {
  outline: none;
  border-color: hsl(0 0% 3.9%);
  box-shadow: 0 0 0 2px hsl(0 0% 3.9% / 0.1);
}

.filter-select:disabled {
  background-color: hsl(0 0% 96.1%);
  color: hsl(0 0% 45.1%);
  cursor: not-allowed;
  opacity: 0.5;
}

.filter-select option {
  padding: 0.5rem;
  color: hsl(0 0% 3.9%);
  background-color: hsl(0 0% 100%);
}

.filter-select option:hover,
.filter-select option:focus {
  background-color: hsl(0 0% 96.1%);
}

/* Responsive design */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1.5rem;
    margin: 1rem;
    max-width: calc(100vw - 2rem);
  }

  .filters-section {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .filter-group {
    min-width: 100%;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 1rem;
    margin: 0.5rem;
    max-width: calc(100vw - 1rem);
  }

  .filters-section {
    padding: 1rem;
    gap: 0.75rem;
  }

  .filter-select {
    height: 2.25rem;
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }
}
</style>
