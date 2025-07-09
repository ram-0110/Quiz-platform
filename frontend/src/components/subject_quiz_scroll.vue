<!-- subject_quiz_scroll -->
<template>
  <div class="subject-container subject-selector">
    <div class="d-flex justify-content-between align-items-center title-text header">
      <h2 class="title m-0 p-0">{{ props.subject.name }}</h2>
      <router-link class="view-all pt-2" to="/about" v-if="obj_subj && obj_subj.length > 0">
        View all <span class="view-icon">›</span>
      </router-link>
    </div>

    <!-- <hr class="divider-line" /> -->

    <div class="scroll-container-wrapper mt-2">
      <button
        class="scroll-button left"
        @click="scrollLeft"
        v-show="showLeft"
        aria-label="Scroll left"
      >
        <span class="arrow-icon">‹</span>
      </button>

      <div class="scroll-wrapper" ref="scrollArea" @scroll="handleScroll">
        <div class="scroll-container">
          <div v-if="!obj_subj || obj_subj.length === 0" class="empty-state mt-2 ms-3">
            No quizzes available
          </div>
          <div v-else class="quiz-items">
            <div v-for="(item, index) in obj_subj" :key="index">
              <quiz-card-scroll :item="item" />
            </div>
          </div>
        </div>
      </div>

      <button
        class="scroll-button right"
        @click="scrollRight"
        v-show="showRight"
        aria-label="Scroll right"
      >
        <span class="arrow-icon">›</span>
      </button>
    </div>

    <!-- <div
      v-if="obj_subj && obj_subj.length > 0"
      class="d-flex align-items-center ms-3 progress-bar-area"
    >
      <h5 class="course-footer me-3 mb-0"></h5>
      <div class="progress minimal-progress">
        <div
          class="progress-bar"
          role="progressbar"
          :style="`width: 100%; background-color: #000000`"
          aria-valuenow="50"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
    </div> -->

    <!-- <hr class="divider-line" /> -->
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import QuizCardScroll from './quiz_card_scroll.vue'
import api from '@/axios/axios'

const props = defineProps(['subject'])
const obj_subj = ref(null)

onMounted(async () => {
  try {
    const response = await api.get('/dashboard-sub-quiz', {
      params: { subjectid: props.subject.id },
    })
    obj_subj.value = response.data.results
  } catch (error) {
    console.error('Error fetching sub-quiz:', error)
  }
})

// ---------------------------animation---------------------------------------------------------------------
const scrollArea = ref(null)
const showLeft = ref(false)
const showRight = ref(true)
const CARD_WIDTH = 210 // 200px card width + 10px gap

/**
 * Scroll the container left by 5 card widths
 */
function scrollLeft() {
  if (!scrollArea.value) return

  scrollArea.value.scrollBy({
    left: -CARD_WIDTH * 5,
    behavior: 'smooth',
  })
}

/**
 * Scroll the container right by 5 card widths
 */
function scrollRight() {
  if (!scrollArea.value) return

  scrollArea.value.scrollBy({
    left: CARD_WIDTH * 5,
    behavior: 'smooth',
  })
}

function handleScroll() {
  const el = scrollArea.value
  if (!el) return

  showLeft.value = el.scrollLeft > 0
  showRight.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 1
}

onMounted(() => {
  nextTick(() => handleScroll())

  window.addEventListener('resize', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleScroll)
})
// ------------------------------------------------------------------------------------------------
</script>

<style scoped>
.progress-bar-area {
  border-top: 1px solid #e2e2e2;
  padding-top: 1.1rem;
  margin-top: 1rem;
}
.title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e2e2;
}
/* Subject selector styles */
.subject-selector {
  margin-bottom: 2rem;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  padding: 1.5rem;
  background-color: #fff;
}

.subject-selector .title {
  font-size: 1.25rem;
}

.subject-container {
  margin-bottom: 1rem;
}

.minimal-progress {
  height: 6px;
  background-color: #f5f5f5; /* Slightly lighter grey background */
  border-radius: 30px;
  overflow: hidden;
  width: 80%;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.minimal-progress .progress-bar {
  border-radius: 30px;
  transition: width 0.4s ease-in-out;
}

.course-title {
  font-size: 1.2rem;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.view-all {
  font-size: 0.9rem;
  color: #000000;
  text-decoration: none;
  text-align: right;
  margin-right: 5rem;
  display: flex;
  align-items: center;
  transition: opacity 0.2s;
}

.view-all:hover {
  opacity: 0.7;
}

.view-icon {
  margin-left: 3px;
  font-size: 1.1rem;
}

.course-footer {
  font-size: 1rem;
  font-weight: 400;
  color: #212121;
}

.title-text {
  margin-bottom: 0;
}

.scroll-container-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 96%;
  padding-top: 0;
}

.scroll-button {
  position: absolute;
  z-index: 2;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 50%;
  transform: translateY(-50%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.arrow-icon {
  font-size: 1.4rem;
  line-height: 1;
}

.scroll-button:hover {
  background-color: #fafafa;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

.scroll-button:active {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transform: translateY(-50%) scale(0.98);
}

.scroll-button.left {
  left: 0;
}

.scroll-button.right {
  right: 0;
}

.scroll-wrapper {
  overflow-x: auto;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
  flex: 1;
  position: relative;
  padding: 0.5rem 0;
}

.scroll-wrapper::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}

.scroll-container {
  display: flex;
  gap: 10px;
  width: max-content;
  padding: 0 2rem;
}

.quiz-items {
  display: flex;
  gap: 10px;
}

.empty-state {
  color: #757575;
  font-style: italic;
}

.divider-line {
  margin-top: 1rem;
  margin-bottom: 2.2rem;
  border-color: #e2e2e2;
  opacity: 0.8;
  border-width: 1px;
}
</style>
