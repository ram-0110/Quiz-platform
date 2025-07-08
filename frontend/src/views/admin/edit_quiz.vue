<template>
  <div class="dashboard-container bg-white border rounded-lg p-4">
    <div class="header border-bottom pb-3 mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="title text-black fw-bold">Edit Quiz</h1>
          <p class="subtitle text-dark">Edit your quiz</p>
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
          <label class="form-label fw-bold text-black mb-2">
            <i class="bi bi-book me-1"></i> Subject Name
          </label>
          <div class="form-control" readonly>{{ subjectName }}</div>
        </div>
        <div class="flex-grow-1">
          <label class="form-label fw-bold text-black mb-2">
            <i class="bi bi-bookmark me-1"></i> Chapter Name
          </label>
          <div class="form-control" readonly>{{ chapterName }}</div>
        </div>
        <div class="flex-grow-1">
          <label class="form-label fw-bold text-black mb-2">
            <i class="bi bi-bookmark me-1"></i> Quiz Name
          </label>
          <div class="form-control" readonly>{{ quizName }}</div>
        </div>
      </div>
    </div>

    <div class="questions-container">
      <div v-if="questions.length > 0" class="mb-3">
        <h3 class="fs-5 fw-bold mb-3 d-flex align-items-center">
          <span class="badge bg-black rounded-pill me-2">{{ questions.length }}</span>
          Question{{ questions.length !== 1 ? 's' : '' }}
        </h3>

        <div v-for="(question, index) in questions" :key="question.id" class="question-wrapper">
          <p>{{ question.correctOption }}</p>
          <div v-if="question.correctOption < 10">
            <Single_Option
              :index="index + 1"
              :initialQuestion="question"
              :type="question.type"
              @remove="removeQuestionById(question.id)"
              @problem="updateQuestion(index, $event)"
            />
          </div>
          <div v-else="question.correctOption">
            <multiple_option
              :index="index + 1"
              :initialQuestion="question"
              :type="question.type"
              @remove="removeQuestionById(question.id)"
              @problem="updateQuestion(index, $event)"
            />
          </div>
        </div>
      </div>

      <div v-else class="empty-state text-center py-5">
        <p class="text-muted">No questions added yet. Click "Add Question" to begin.</p>
      </div>

      <div class="d-flex flex-wrap justify-content-between gap-2 mt-4">
        <button class="btn btn-outline-dark" @click="addSingleOption">
          <i class="bi bi-plus-circle me-1"></i> Add single option
        </button>
        <button class="btn btn-outline-dark" @click="addMultipleOption">
          <i class="bi bi-plus-circle me-1"></i> Add multiple option
        </button>
        <button class="btn btn-black" @click="saveQuiz" :disabled="!isFormValid">
          <i class="bi bi-save me-1"></i> Save Quiz
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Single_Option from '@/components/admin/Single_Option.vue'
import multiple_option from '@/components/admin/multiple_option.vue'
import api from '@/axios/axios'

const route = useRoute()
const router = useRouter()
const quizId = route.params.id

const subjectName = ref('')
const chapterName = ref('')
const quizName = ref('')
const questions = ref([])
const problem = ref([])

let nextId = 1 // Track IDs for new questions

onMounted(async () => {
  try {
    const response = await api.get('http://127.0.0.1:5000/api/get-quiz', {
      params: { id: quizId },
    })
    const quizData = response.data

    subjectName.value = quizData.subject
    chapterName.value = quizData.chapter
    quizName.value = quizData.quiz

    questions.value = quizData.problem.map((item, index) => {
      return {
        id: index + 1,
        question: item.question_statement,
        options: [item.option1, item.option2, item.option3, item.option4],
        correctOption: item.correct_option,
        type: 'single-choice', // Or determine type if your API supports both
      }
    })

    problem.value = [...questions.value]
    nextId = questions.value.length + 1
  } catch (error) {
    console.error('Error fetching quiz data:', error)
  }
})

const isFormValid = computed(() => {
  return (
    subjectName.value.trim() !== '' && chapterName.value.trim() !== '' && questions.value.length > 0
  )
})

const updateQuestion = (index, question) => {
  problem.value[index] = question
}

const addSingleOption = () => {
  const newQuestion = {
    id: nextId++,
    type: 'single-choice',
    question: '',
    options: ['', '', '', ''],
    correctOption: '',
  }
  questions.value.push(newQuestion)
  problem.value.push(newQuestion)
}

const addMultipleOption = () => {
  const newQuestion = {
    id: nextId++,
    type: 'multiple-choice',
    question: '',
    options: ['', '', '', ''],
    correctOptions: [],
    hasCorrectOption: false,
  }
  questions.value.push(newQuestion)
  problem.value.push(newQuestion)
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
    alert('Please complete the form and add at least one question.')
    return
  }

  try {
    const response = await api.post('/update-quiz', {
      subject: subjectName.value,
      chapter: chapterName.value,
      quiz: quizName.value,
      problem: problem.value,
    })
    console.log('Quiz saved successfully:', response.data)
    router.push('/admin')
  } catch (error) {
    console.error('Error saving quiz:', error)
  }
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
</style>
