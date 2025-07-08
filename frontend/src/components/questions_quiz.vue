<!-- questions_quiz.vue -->
<template>
  <div class="question-container">
    <div class="question-header">
      <span class="question-number">Question 1</span>
      <span class="question-type">Multiple Choice</span>
    </div>

    <h4 class="question-text">What is the powerhouse of the cell?</h4>

    <div class="options-container">
      <div
        v-for="(option, index) in options"
        :key="index"
        class="option"
        :class="{ 'option-selected': selectedOption === index }"
        @click="selectOption(index)"
      >
        <div class="radio-container">
          <input
            type="radio"
            :id="'option' + index"
            name="cell-question"
            :value="option"
            :checked="selectedOption === index"
            @change="selectOption(index)"
          />
          <span class="custom-radio"></span>
        </div>
        <label :for="'option' + index" class="option-label">{{ option }}</label>
      </div>
    </div>

    <div class="question-footer" v-if="showHints">
      <div class="hint-container">
        <button class="hint-button" @click="toggleHint" v-if="!hintVisible">
          <i class="bi bi-lightbulb"></i> Show Hint
        </button>
        <div class="hint-text" v-if="hintVisible">
          <i class="bi bi-lightbulb-fill"></i>
          <span
            >This organelle is responsible for cellular respiration and producing energy in the form
            of ATP.</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const options = ref(['Mitochondria', 'Nucleus', 'Chloroplast', 'Ribosome'])
const selectedOption = ref(null)
const showHints = ref(true)
const hintVisible = ref(false)

const selectOption = (index) => {
  selectedOption.value = index
}

const toggleHint = () => {
  hintVisible.value = !hintVisible.value
}
</script>

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

.options-container {
  margin: 1.25rem 0;
}

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

.option:hover {
  background-color: #f9f9f9;
  border-color: #d0d0d0;
  transform: translateX(2px);
}

.option-selected {
  background-color: #f0f0f0;
  border-color: #c0c0c0;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.radio-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  margin-right: 10px;
}

input[type='radio'] {
  opacity: 0;
  position: absolute;
  width: 18px;
  height: 18px;
  margin: 0;
  cursor: pointer;
  z-index: 2;
}

.custom-radio {
  position: absolute;
  top: 0;
  left: 0;
  width: 18px;
  height: 18px;
  border: 2px solid #aaa;
  border-radius: 50%;
  transition: all 0.2s ease;
}

input[type='radio']:checked + .custom-radio {
  border: 2px solid #000;
}

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

.option-label {
  flex: 1;
  cursor: pointer;
  font-size: 0.95rem;
  line-height: 1.4;
  color: #333;
  padding: 0.15rem 0;
  margin-bottom: 0;
}

.question-footer {
  margin-top: 1.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.hint-container {
  display: flex;
  justify-content: flex-start;
}

.hint-button {
  background: none;
  border: none;
  color: #666;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.hint-button:hover {
  background-color: #f5f5f5;
  color: #000;
}

.hint-text {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  background-color: #fffde7;
  border: 1px solid #fff9c4;
  border-radius: 5px;
  padding: 0.6rem 0.8rem;
  font-size: 0.85rem;
  color: #666;
  line-height: 1.5;
}

.bi-lightbulb,
.bi-lightbulb-fill {
  font-size: 0.9rem;
  color: #ffc107;
}

@media (max-width: 576px) {
  .option {
    padding: 0.6rem 0.8rem;
  }

  .question-text {
    font-size: 1rem;
  }
}
</style>
