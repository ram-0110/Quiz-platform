<!-- add_quiz.vue -->

<template>
  <div class="dashboard-container bg-white border rounded-lg p-4">
    <div class="header border-bottom pb-3 mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="title text-black fw-bold">Create Quiz</h1>
          <p class="subtitle text-dark">Add questions and answers to your quiz</p>
        </div>
        <div class="quiz-icon d-none d-md-block">
          <i class="bi bi-pencil-square fs-1"></i>
        </div>
      </div>
    </div>

    <div class="subject-selector border rounded-lg p-4 mb-4 bg-light">
      <div class="mb-3">
        <h3 class="fs-5 fw-bold mb-3 text-black">Quiz Details</h3>
      </div>
      <div class="d-flex flex-wrap gap-3 mb-2">
        <div class="flex-grow-1">
          <label for="subjectName" class="form-label fw-bold text-black mb-2">
            <i class="bi bi-book me-1"></i> Subject Name
          </label>
          <input
            type="text"
            id="subjectName"
            class="form-control"
            placeholder="Enter subject name"
            v-model="subjectName"
            required
          />
        </div>
        <div class="flex-grow-1">
          <label for="chapterName" class="form-label fw-bold text-black mb-2">
            <i class="bi bi-bookmark me-1"></i> Chapter Name
          </label>
          <input
            type="text"
            id="chapterName"
            class="form-control"
            placeholder="Enter chapter name"
            v-model="chapterName"
            required
          />
        </div>
        <div class="flex-grow-1">
          <label for="quizName" class="form-label fw-bold text-black mb-2">
            <i class="bi bi-bookmark me-1"></i> Quiz Name
          </label>
          <input
            type="text"
            id="quizName"
            class="form-control"
            placeholder="Enter quiz name"
            v-model="quizName"
            required
          />
        </div>
      </div>
      <div class="quiz-meta mt-3">
        <p class="form-text text-dark m-0">
          <small>Questions: {{ questions.length }} | Last edited: {{ currentDate }}</small>
        </p>
      </div>
    </div>

    <div class="questions-container">
      <div v-if="questions.length > 0" class="mb-3">
        <h3 class="fs-5 fw-bold mb-3 d-flex align-items-center">
          <span class="badge bg-black rounded-pill me-2">{{ questions.length }}</span>
          Question{{ questions.length !== 1 ? 's' : '' }}
        </h3>
        <div v-for="(question, index) in questions" :key="question.id" class="question-wrapper">
          <Single_Option
            :index="index + 1"
            v-model:question="questions[index]"
            :type="question.type"
            @remove="removeQuestionById(question.id)"
            @problem="updateQuestion(index, $event)"
          />
        </div>

        <div v-if="questions.length === 0" class="empty-state text-center py-5">
          <p class="text-muted">No questions added yet. Click "Add Question" to begin.</p>
        </div>
      </div>

      <div class="d-flex flex-wrap justify-content-between gap-2 mt-4">
        <button class="btn btn-outline-dark" @click="addSingleOption">
          <i class="bi bi-plus-circle me-1"></i> Add single option
        </button>
 
        <button class="btn btn-black" @click="saveQuiz" :disabled="!isFormValid">
          <i class="bi bi-save me-1"></i> Save Quiz
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Single_Option from '@/components/admin/Single_Option.vue'
import api from '@/axios/axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification' // ✅ import toast

const toast = useToast() // ✅ initialize toast
const router = useRouter()
const problem = ref([])

const updateQuestion = (index, question) => {
  problem.value[index] = question
}

const subjectName = ref('')
const chapterName = ref('')
const quizName = ref('')
const questions = ref([])
let nextId = 1

const isFormValid = computed(() => {
  return (
    subjectName.value.trim() !== '' && chapterName.value.trim() !== '' && questions.value.length > 0
  )
})

const currentDate = computed(() =>
  new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }),
)

const addSingleOption = () => {
  questions.value.push({
    id: nextId++,
    type: 'single-choice',
    text: '',
    options: [],
    correctAnswer: null,
  })
}

const addMultipleOption = () => {
  questions.value.push({
    id: nextId++,
    type: 'multiple-choice',
    text: '',
    options: [],
    correctAnswers: [],
  })
}

const removeQuestionById = (id) => {
  const idx = questions.value.findIndex((q) => q.id === id)
  if (idx !== -1) {
    questions.value.splice(idx, 1)
    problem.value.splice(idx, 1)
  }
}

const saveQuiz = async () => {
  if (!isFormValid.value) {
    toast.warning('Please complete the form and add at least one question.') // ✅ replaces alert
    return
  }

  try {
    const response = await api.post('/add-quizzes', {
      subject: subjectName.value,
      chapter: chapterName.value,
      quiz: quizName.value,
      problem: problem.value,
    })
    console.log('Quiz saved successfully:', response.data)
    toast.success('Quiz saved successfully!') // ✅ success toast
    router.push('/admin')
  } catch (error) {
    console.error('Error saving quiz:', error)
    toast.error('Failed to save quiz') // ✅ error toast
  }

  console.log('Quiz saved', {
    subject: subjectName.value,
    chapter: chapterName.value,
    problem: problem.value,
  })
}
</script>

<style scoped>
.dashboard-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #000;
  background-color: #fff;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e2e2e2;
}

/* rest of styling unchanged */
</style>
