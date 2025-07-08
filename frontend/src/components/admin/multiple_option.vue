<template>
  <div class="question-card rounded shadow-sm p-4 mb-4 bg-white">
    <h2 class="fw-bold mb-4 text-black d-flex align-items-center">
      <span class="question-number me-2">{{ index }}</span>
      Multiple Choice Question
    </h2>

    <textarea
      name="question"
      id="question"
      class="form-control mb-4"
      rows="3"
      placeholder="Enter your multiple choice question here..."
      v-model="question"
    ></textarea>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3 class="fw-bold mb-0 text-black">Options</h3>
      <div><small class="text-muted ms-2">All fields required</small></div>
    </div>

    <div class="option-container">
      <div v-for="(option, idx) in options" :key="idx" class="input-group mb-3 option-input">
        <span class="input-group-text bg-black text-white">{{ idx + 1 }}</span>
        <input
          type="text"
          :id="'option' + (idx + 1)"
          class="form-control"
          :placeholder="'Option ' + (idx + 1)"
          v-model="options[idx]"
          required
        />
        <div class="input-group-text">
          <div class="form-check">
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
    </div>

    <div class="alert alert-info mt-3" v-if="!hasCorrectOption">
      <i class="bi bi-info-circle me-2"></i>Please select at least one correct option
    </div>

    <div class="d-flex justify-content-end mt-4">
      <button class="btn btn-outline-dark me-2" @click="$emit('remove')">
        <i class="bi bi-trash me-1"></i>Remove
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, watch, computed } from 'vue'

const props = defineProps({
  index: {
    type: Number,
    default: 1,
  },
  type: {
    type: String,
    default: 'multiple-choice',
  },
  initialQuestion: {
    type: Object,
    default: () => ({
      question: '',
      options: ['', '', '', ''],
      correctOptions: [],
    }),
  },
})

const emit = defineEmits(['problem', 'remove'])

// Initialize refs using initialQuestion
const question = ref(props.initialQuestion.question || '')
const options = ref([...props.initialQuestion.options])
const correctOptions = ref([...(props.initialQuestion.correctOptions || [])])

const hasCorrectOption = computed(() => correctOptions.value.length > 0)

function toggleCorrectOption(index) {
  const optionNumber = index + 1
  const position = correctOptions.value.indexOf(optionNumber)

  if (position === -1) {
    correctOptions.value.push(optionNumber)
  } else {
    correctOptions.value.splice(position, 1)
  }
}

// Watch changes and emit full question object
watch(
  [question, options, correctOptions],
  () => {
    emit('problem', {
      question: question.value,
      options: options.value,
      correctOptions: correctOptions.value,
      hasCorrectOption: hasCorrectOption.value,
      type: 'multiple-choice',
    })
  },
  { deep: true },
)
</script>

<style scoped>
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

textarea#question:focus {
  border-color: #000 !important;
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

.btn-outline-danger {
  transition: all 0.2s ease;
}

h2,
h3 {
  font-size: 1.25rem;
}

.input-group-text {
  justify-content: center;
  border: 1px solid #e2e2e2 !important;
}

.input-group-text:first-child {
  width: 40px;
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

.form-switch .form-check-input:focus {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23000'/%3e%3c/svg%3e");
}

.form-switch .form-check-input:checked {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23fff'/%3e%3c/svg%3e");
}
</style>
