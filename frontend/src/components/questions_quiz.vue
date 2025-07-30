<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  question: Object,
  selected: [Number, Array],
})

const emit = defineEmits(['select'])

const isMultipleChoice = computed(() => props.question.correct_option >= 10)

const selectedOption = ref(
  isMultipleChoice.value ? [...(props.selected || [])] : (props.selected ?? null),
)

watch(
  () => props.selected,
  (val) => {
    selectedOption.value = isMultipleChoice.value ? [...(val || [])] : val
  },
)

const dynamicOptions = computed(() => {
  return [
    props.question.option1,
    props.question.option2,
    props.question.option3,
    props.question.option4,
  ].filter(Boolean)
})

const toggleOption = (index) => {
  if (isMultipleChoice.value) {
    const current = [...selectedOption.value]
    const idx = current.indexOf(index)
    if (idx >= 0) {
      current.splice(idx, 1) // remove
    } else {
      current.push(index) // add
    }
    selectedOption.value = current
    emit('select', current)
  } else {
    selectedOption.value = index
    emit('select', index)
  }
}
</script>

<template>
  <div class="question-container">
    <div class="question-header">
      <span class="question-number">Question</span>
      <span class="question-type">{{
        isMultipleChoice ? 'Multiple Choice' : 'Single Choice'
      }}</span>
    </div>

    <h4 class="question-text">{{ question.question_statement }}</h4>

    <div
      v-for="(option, index) in dynamicOptions"
      :key="index"
      class="option"
      :class="{
        'option-selected': isMultipleChoice
          ? selectedOption.includes(index)
          : selectedOption === index,
      }"
      @click="toggleOption(index)"
    >
      <div class="radio-container">
        <input
          :type="isMultipleChoice ? 'checkbox' : 'radio'"
          :id="'option' + index"
          :name="'question' + question.id"
          :checked="isMultipleChoice ? selectedOption.includes(index) : selectedOption === index"
          @change="toggleOption(index)"
        />
        <span :class="isMultipleChoice ? 'custom-checkbox' : 'custom-radio'"></span>
      </div>
      <label :for="'option' + index" class="option-label">{{ option }}</label>
    </div>
  </div>
</template>

<style scoped>
.question-container {
  max-width: 650px;
  margin: 0 auto;
  padding: 1rem 0.75rem;
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    sans-serif;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-number {
  font-size: 0.8rem;
  font-weight: 600;
  color: #000;
  background-color: #f8f8f8;
  padding: 0.25rem 0.6rem;
  border-radius: 16px;
  border: 1px solid #eaeaea;
}

.question-type {
  font-size: 0.75rem;
  color: #666;
}

.question-text {
  font-size: 1.1rem;
  font-weight: 500;
  line-height: 1.4;
  margin-bottom: 1.25rem;
  color: #212121;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.radio-container {
  position: relative;
  width: 20px;
  height: 20px;
  margin-right: 12px;
}

/* Hide native input */
input[type='radio'],
input[type='checkbox'] {
  opacity: 0;
  position: absolute;
  width: 20px;
  height: 20px;
  margin: 0;
  cursor: pointer;
  z-index: 2;
}

/* Base for both */
.custom-radio,
.custom-checkbox {
  position: absolute;
  top: 0;
  left: 0;
  width: 18px;
  height: 18px;
  background-color: #fff;
  border: 2px solid #aaa;
  transition: all 0.2s ease;
}

/* Radio style */
.custom-radio {
  border-radius: 50%;
}

/* Checkbox style */
.custom-checkbox {
  border-radius: 4px;
}

/* Selected radio */
input[type='radio']:checked + .custom-radio::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #000;
}

/* Selected checkbox */
input[type='checkbox']:checked + .custom-checkbox {
  background-color: #000;
  border-color: #000;
}

input[type='checkbox']:checked + .custom-checkbox::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 5px;
  width: 4px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* Option container */
.option {
  display: flex;
  align-items: center;
  padding: 0.7rem 1rem;
  margin-bottom: 0.6rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: #fff;
  transition: all 0.2s ease;
  cursor: pointer;
}

.option-selected {
  background-color: #f0f0f0;
  border-color: #c0c0c0;
}

.option-label {
  flex: 1;
  cursor: pointer;
  font-size: 0.95rem;
  line-height: 1.4;
  color: #333;
  padding: 0.15rem 0;
  margin-bottom: 0;
}
</style>
