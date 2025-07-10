<!-- SubjectProgress.vue -->
<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h5 class="fw-bold text-dark m-0">{{ label }}</h5>
    <span class="badge bg-primary text-white fs-6">{{ attempted }}/{{ total }}</span>
  </div>

  <div class="position-relative mb-4">
    <div class="progress" style="height: 24px; border-radius: 12px">
      <div
        class="progress-bar text-white"
        role="progressbar"
        :style="{ width: progressPercent + '%', background: getGradientColor() }"
      >
        <span class="fw-bold ps-2">{{ progressPercent }}%</span>
      </div>
    </div>
  </div>

  <div v-if="showChart && chapterQuizzes.length" class="border rounded p-3 mb-4 chart-wrapper">
    <h6 class="mb-3 text-center text-dark">Chapter-wise Quiz Details</h6>
    <div class="chart-scroll-wrapper">
      <canvas ref="chartCanvas" class="w-100" height="300"></canvas>
    </div>
  </div>

  <div class="row text-center">
    <div class="col">
      <div class="text-muted">Completed</div>
      <div class="fw-bold text-dark fs-5">{{ attempted }}</div>
    </div>
    <div class="col">
      <div class="text-muted">Remaining</div>
      <div class="fw-bold text-dark fs-5">{{ remaining }}</div>
    </div>
    <div class="col">
      <div class="text-muted">Progress</div>
      <div class="fw-bold text-dark fs-5">{{ progressPercent }}%</div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch, nextTick } from 'vue'

const props = defineProps({
  label: { type: String, default: 'Subject Progress' },
  attempted: { type: Number, default: 0 },
  total: { type: Number, default: 0 },
  showChart: { type: Boolean, default: true },
  animated: { type: Boolean, default: true },
  chapterQuizzes: {
    type: Array,
    default: () => [],
  },
})

const chartCanvas = ref(null)
let chartInstance = null

const progressPercent = computed(() =>
  props.total > 0 ? Math.round((props.attempted / props.total) * 100) : 0,
)

const remaining = computed(() => Math.max(0, props.total - props.attempted))

const getGradientColor = () => {
  return '#9ec5fe' // subtle blue for progress bar
}

const initChart = async () => {
  if (!props.showChart || !chartCanvas.value || props.chapterQuizzes.length === 0) return

  const { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } = await import(
    'chart.js'
  )
  Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

  const ctx = chartCanvas.value.getContext('2d')
  if (!ctx) return

  if (chartInstance) chartInstance.destroy()

  const labels = props.chapterQuizzes.map((q) => q.chapter_name)
  const attempted = props.chapterQuizzes.map((q) => q.attempted_quizzes)
  const total = props.chapterQuizzes.map((q) => q.total_quizzes)
  const remaining = total.map((t, i) => Math.max(0, t - attempted[i]))

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Attempted',
          data: attempted,
          backgroundColor: '#9ec5fe',
        },
        {
          label: 'Remaining',
          data: remaining,
          backgroundColor: '#dee2e6',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: '#333' } },
        tooltip: {
          callbacks: {
            label(context) {
              const attemptedVal = context.dataset.data[context.dataIndex]
              const totalVal = props.chapterQuizzes[context.dataIndex]?.total_quizzes || 0
              const percentage = totalVal ? Math.round((attemptedVal / totalVal) * 100) : 0
              return `${attemptedVal} quizzes (${percentage}%)`
            },
          },
          backgroundColor: '#333333',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, color: '#333' },
          grid: { color: 'rgba(0,0,0,0.05)' },
        },
        x: {
          ticks: { color: '#333' },
          grid: { color: 'rgba(0,0,0,0.05)' },
        },
      },
      animation: {
        duration: props.animated ? 1000 : 0,
      },
    },
  })
}

onMounted(() => {
  nextTick(() => {
    setTimeout(initChart, 100)
  })
})

watch(() => props.chapterQuizzes, initChart, { deep: true })
</script>

<style scoped>
.chart-scroll-wrapper {
  max-height: 200px;
  overflow-y: auto;
}
</style>
