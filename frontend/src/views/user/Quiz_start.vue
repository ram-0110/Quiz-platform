<!-- quiz_start.vue -->
<template>
  <div class="quiz-container py-3">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-3 quiz-header">
      <h4 class="mb-0 fw-medium quiz-title">Quiz 1: Optics</h4>
      <div class="time-display">
        <i class="bi bi-clock me-1"></i>
        <span class="timer">10:00</span>
      </div>
    </div>

    <!-- Question Card -->
    <div class="card quiz-card mb-4">
      <div class="card-body p-3 p-lg-4">
        <Questions />
        <div class="mt-3 d-flex gap-2 action-buttons">
          <div class="d-flex gap-2 me-auto">
            <button class="btn btn-outline-secondary btn-sm">
              <span class="btn-text">Clear</span>
            </button>
            <button class="btn btn-outline-secondary btn-sm">
              <span class="btn-text">Save & Next</span>
            </button>
          </div>
          <button class="btn btn-primary-dark btn-sm">Submit</button>
        </div>
      </div>
    </div>

    <!-- Progress & Navigation -->
    <div class="text-center mt-4 footer-quiz">
      <div class="d-flex align-items-center justify-content-center mb-2">
        <span class="progress-text me-2">Progress</span>
        <div class="progress rounded-pill mb-0" style="height: 4px; width: 40%">
          <div
            class="progress-bar"
            role="progressbar"
            style="width: 50%"
            aria-valuenow="50"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>
        <span class="progress-percentage ms-2">50%</span>
      </div>
      <div class="d-flex justify-content-center flex-wrap gap-1 nav-dots mt-3">
        <button
          v-for="n in 10"
          :key="n"
          class="btn question-nav-btn"
          :class="n === 5 ? 'active' : ''"
        >
          {{ n }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/axios/axios'
import Questions from '@/components/questions_quiz.vue'

const route = useRoute()

onMounted(async () => {
  const quiz_id = route.params.quiz_id
  try {
    const response = await api.get(`/quiz/${quiz_id}`)
    console.log(response.data)
  } catch (error) {
    console.error('Error fetching quiz:', error)
  }
})
</script>

<style scoped>
.quiz-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header */
.quiz-header {
  max-width: 700px;
  margin: 0 auto 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.quiz-title {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  color: #212121;
}

.time-display {
  display: flex;
  align-items: center;
  padding: 0.3rem 0.75rem;
  background-color: #f8f8f8;
  border-radius: 1.25rem;
  border: 1px solid #f0f0f0;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.time-display:hover {
  background-color: #f0f0f0;
}

.timer {
  font-weight: 500;
  color: #333;
  font-family: monospace;
  font-size: 0.95rem;
}

/* Question Card */
.quiz-card {
  border: none;
  border-radius: 0.75rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  max-width: 700px;
  margin: 0 auto 1.5rem;
  transition: box-shadow 0.3s;
}

.quiz-card:hover {
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.1);
}

/* Buttons */
.action-buttons {
  margin-top: 1.5rem;
}

.btn {
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-sm {
  padding: 0.35rem 0.8rem;
  font-size: 0.875rem;
}

.btn-outline-secondary {
  border-color: #dee2e6;
  color: #495057;
  background-color: transparent;
  min-width: 80px;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #212529;
  border-color: #ced4da;
}

.btn-primary-dark {
  background-color: #000;
  color: #fff;
  border: none;
  min-width: 80px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-primary-dark:hover {
  background-color: #222;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
}

.btn-primary-dark:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

.btn-text {
  white-space: nowrap;
}

/* Footer */
.footer-quiz {
  max-width: 700px;
  margin: 2rem auto 0;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.progress {
  background-color: #f1f1f1;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03);
}

.progress-bar {
  background-color: #000;
  border-radius: 30px;
  transition: width 0.4s ease-in-out;
}

.progress-text,
.progress-percentage {
  font-size: 0.8rem;
  color: #666;
  font-weight: 500;
}

/* Navigation dots */
.nav-dots {
  margin-top: 1rem;
}

.question-nav-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 500;
  border-radius: 50%;
  border: 1px solid #e0e0e0;
  background-color: #fff;
  color: #333;
  transition: all 0.2s ease;
}

.question-nav-btn:hover {
  background-color: #f5f5f5;
  border-color: #ccc;
  transform: translateY(-1px);
}

.question-nav-btn.active {
  background-color: #000;
  color: #fff;
  border-color: #000;
}

/* Icon spacing */
.bi-clock {
  font-size: 0.95rem;
  color: #555;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }

  .action-buttons > div {
    margin-right: 0;
    margin-bottom: 0.75rem;
    width: 100%;
  }

  .action-buttons .btn {
    flex: 1;
  }
}
</style>
