<template>
  <div class="question-card rounded shadow-sm p-4 mb-4 bg-white">
    <h2 class="fw-bold mb-4 text-black d-flex align-items-center">
      <span class="question-number me-2">{{ index }}</span>
      {{ type === 'single-choice' ? 'Question' : 'Multiple Choice Question' }}
    </h2>

    <!-- Question Input -->
    <textarea
      name="question"
      id="question"
      class="form-control mb-4"
      rows="3"
      :placeholder="
        type === 'single-choice'
          ? 'Enter your question here...'
          : 'Enter your multiple choice question here...'
      "
      v-model="question"
    ></textarea>

    <!-- Options Input -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3 class="fw-bold mb-0 text-black">Options</h3>
      <small class="text-muted">All fields required</small>
    </div>

    <div class="option-container">
      <div
        v-for="(option, idx) in options"
        :key="idx"
        class="d-flex align-items-center gap-3 mb-3 option-input"
      >
        <div class="input-group flex-grow-1">
          <span class="input-group-text bg-black text-white">{{ idx + 1 }}</span>
          <input
            type="text"
            :id="'option' + (idx + 1)"
            class="form-control"
            :placeholder="'Option ' + (idx + 1)"
            v-model="options[idx]"
            required
          />
        </div>

        <!-- Checkbox for multiple-choice -->
        <div v-if="type === 'multiple-choice'" class="form-check ms-2">
          <input
            class="form-check-input"
            type="checkbox"
            :id="'correct' + (idx + 1)"
            @change="toggleCorrectOption(idx)"
            :checked="correctOptions.includes(idx + 1)"
          />
          <label class="form-check-label" :for="'correct' + (idx + 1)"> Correct </label>
        </div>
      </div>
    </div>

    <!-- Dropdown for single correct option -->
    <div v-if="type === 'single-choice'" class="mb-3">
      <h3 class="fw-bold mb-0 text-black">Correct Option</h3>
      <div class="input-group mt-2">
        <span class="input-group-text bg-black text-white">#</span>
        <select class="form-select" v-model="correctOption" aria-label="Select correct answer">
          <option value="" disabled>Select correct option</option>
          <option v-for="idx in options.length" :key="idx" :value="idx">Option {{ idx }}</option>
        </select>
      </div>
    </div>

    <!-- Info for missing correct selection -->
    <div class="alert alert-info mt-3" v-if="type === 'multiple-choice' && !hasCorrectOption">
      <i class="bi bi-info-circle me-2"></i>Please select at least one correct option
    </div>

    <!-- Remove button -->
    <div class="d-flex justify-content-end mt-4">
      <button class="btn btn-outline-dark me-2" @click="$emit('remove')">
        <i class="bi bi-trash me-1"></i>Remove
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  index: Number,
  type: {
    type: String,
    default: 'single-choice',
  },
  initialQuestion: {
    type: Object,
    default: () => ({
      question: '',
      options: ['', '', '', ''],
      correctOption: '',
      correctOptions: [],
    }),
  },
})

const emit = defineEmits(['problem', 'remove'])

// Initial values
const question = ref(props.initialQuestion.question || '')
const options = ref([...props.initialQuestion.options] || ['', '', '', ''])
const correctOption = ref(props.initialQuestion.correctOption || '')
const correctOptions = ref([...(props.initialQuestion.correctOptions || [])])

// Computed for validation
const hasCorrectOption = computed(() => {
  return correctOptions.value.length > 0
})

// Multiple-choice toggle
function toggleCorrectOption(index) {
  const value = index + 1
  const i = correctOptions.value.indexOf(value)
  if (i === -1) {
    correctOptions.value.push(value)
  } else {
    correctOptions.value.splice(i, 1)
  }
}

// Emit structured question data to parent
watch(
  [question, options, correctOption, correctOptions],
  () => {
    const base = {
      question: question.value,
      options: options.value,
    }

    const data =
      props.type === 'single-choice'
        ? { ...base, correctOption: correctOption.value, type: 'single-choice' }
        : {
            ...base,
            correctOptions: correctOptions.value,
            hasCorrectOption: hasCorrectOption.value,
            type: 'multiple-choice',
          }

    emit('problem', data)
  },
  { deep: true },
)
</script>

<style scoped>
/* Reuse shared styles from your original files */
.question-card {
  border: 1px solid #e2e2e2;
  border-radius: 12px;
  background-color: #fff;
  max-width: 100%;
  transition: all 0.2s ease-in-out;
}

.question-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08) !important;
}

.question-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background-color: #000;
  color: #fff;
  border-radius: 50%;
  font-size: 0.9rem;
}

textarea#question {
  transition: border-color 0.2s ease;
  min-height: 100px;
  border: 1px solid #e2e2e2 !important;
  resize: vertical;
}

textarea:focus,
input:focus,
select:focus {
  box-shadow: 0 0 0 0.25rem rgba(0, 0, 0, 0.1) !important;
  border-color: #000 !important;
}

.btn-outline-dark {
  border: 1px solid #000;
  color: #000;
  transition: all 0.2s ease;
}

.btn-outline-dark:hover {
  background-color: #000;
  color: #fff;
}

h2,
h3 {
  font-size: 1.25rem;
}

.input-group-text {
  width: 40px;
  justify-content: center;
  border: 1px solid #e2e2e2 !important;
}

.option-input:focus-within .input-group-text {
  border-color: #000 !important;
}

.form-control,
.form-select {
  border: 1px solid #e2e2e2 !important;
  transition: all 0.2s ease;
}

.form-control::placeholder {
  color: #999;
  font-style: italic;
}

.option-input {
  transition: transform 0.1s ease;
}

.option-input:focus-within {
  transform: translateX(5px);
}

.form-check-input:checked {
  background-color: #000;
  border-color: #000;
}

.form-check-input:focus {
  border-color: #000;
  box-shadow: 0 0 0 0.25rem rgba(0, 0, 0, 0.1);
}
</style>
