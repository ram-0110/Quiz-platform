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
        <QuestionsQuiz
          v-if="questions.length && questions[active_qes - 1]"
          :question="questions[active_qes - 1]"
          :selected="selectedOptions[active_qes - 1]"
          @select="(selectedIndex) => handleOptionSelect(active_qes - 1, selectedIndex)"
        />

        <div class="mt-3 d-flex gap-2 action-buttons">
          <div class="d-flex gap-2 me-auto">
            <button class="btn btn-outline-secondary btn-sm" @click="clearOption">
              <span class="btn-text">Clear</span>
            </button>
            <button
              class="btn btn-outline-secondary btn-sm"
              @click="nextQuestion"
              :disabled="active_qes === questions.length"
            >
              <span class="btn-text">Save & Next</span>
            </button>
          </div>
          <button
            type="button"
            class="btn btn-primary-dark btn-sm"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
          >
            Submit
          </button>
        </div>
      </div>
    </div>

    <!-- Progress & Navigation -->
    <div class="text-center mt-4 footer-quiz">
      <div class="d-flex justify-content-center flex-wrap gap-1 nav-dots mt-3">
        <button
          v-for="n in questions.length"
          :key="n"
          class="btn question-nav-btn"
          :class="{ active: n === active_qes }"
          @click="setActiveQuestion(n)"
        >
          {{ n }}
        </button>
      </div>
    </div>

    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Conformation</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body"><P>save and sibmit changes once made they cant be undo!!</P></div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary-dark btn-sm" @click="submitQuiz">
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/axios/axios'
import QuestionsQuiz from '@/components/questions_quiz.vue'
import { useToast } from 'vue-toastification' // ✅ import toast

const toast = useToast() // ✅ initialize toast
const route = useRoute()
const router = useRouter()
const active_qes = ref(1)
const questions = ref([])
const selectedOptions = ref([])

const submitQuiz = async () => {
  const quiz_id = route.params.quiz_id
  if (!quiz_id) {
    toast.warning('Quiz ID not found.') // ✅ replaces alert
    return
  }

  const answers = questions.value.map((q, index) => ({
    question_id: q.id,
    selected_option: selectedOptions.value[index] ?? null,
  }))

  try {
    // Hide modal if it's open
    const modalEl = document.getElementById('exampleModal')
    if (modalEl) {
      const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl)
      modalInstance.hide()
    }

    // 🔥 Force-remove modal backdrop and modal-open class from body
    const backdrops = document.querySelectorAll('.modal-backdrop')
    backdrops.forEach((el) => el.remove())

    document.body.classList.remove('modal-open')
    document.body.style.removeProperty('padding-right') // optional

    // Submit the quiz
    await api.post(`/quiz/submit/${quiz_id}/result`, { answers })

    toast.success('Quiz submitted successfully!') // ✅ success toast
    router.push(`/quiz/result/${quiz_id}`)
  } catch (error) {
    console.error('Error submitting quiz:', error)
    toast.error('Failed to submit quiz.') // ✅ error toast
    router.push('/dashboard')
  }
}

const setActiveQuestion = (index) => {
  active_qes.value = index
}

const nextQuestion = () => {
  if (active_qes.value < questions.value.length) {
    active_qes.value++
  }
}

// Function to handle option selection
const handleOptionSelect = (questionIndex, selectedIndex) => {
  selectedOptions.value[questionIndex] = selectedIndex
}

const clearOption = () => {
  selectedOptions.value[active_qes.value - 1] = null
}

onMounted(async () => {
  const quiz_id = route.params.quiz_id
  try {
    const response = await api.get(`/quiz/start/${quiz_id}`)
    questions.value = response.data
    selectedOptions.value = Array(response.data.length).fill(null)
  } catch (error) {
    console.error('Error fetching quiz:', error)
    toast.error('Failed to load quiz.') // ✅ toast on error
  }
})
</script>

<style scoped>
.quiz-container {
  max-width: 900px;
  margin: 5vh auto;
  padding: auto 1rem;
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
