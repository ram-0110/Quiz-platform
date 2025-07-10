<template>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h5 class="fw-bold m-0">{{ label }}</h5>
    <span class="badge bg-primary fs-6">{{ attempted }}/{{ total }}</span>
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
    <!-- Dot & Tooltip -->
    <div
      v-if="progressPercent > 0"
      class="position-absolute translate-middle-x text-center"
      :style="{ left: progressPercent + '%', top: '-20px' }"
    ></div>
  </div>

  <div v-if="showChart" class="border rounded p-3 mb-4 chart-wrapper">
    <canvas ref="chartCanvas" width="300" height="200"></canvas>
  </div>

  <!-- Stats -->
  <div class="row text-center">
    <div class="col">
      <div class="text-muted">Completed</div>
      <div class="fw-bold text-success fs-5">{{ attempted }}</div>
    </div>
    <div class="col">
      <div class="text-muted">Remaining</div>
      <div class="fw-bold text-warning fs-5">{{ remaining }}</div>
    </div>
    <div class="col">
      <div class="text-muted">Progress</div>
      <div class="fw-bold text-primary fs-5">{{ progressPercent }}%</div>
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
})

const chartCanvas = ref(null)
let chartInstance = null

const progressPercent = computed(() =>
  props.total > 0 ? Math.round((props.attempted / props.total) * 100) : 0,
)

const remaining = computed(() => Math.max(0, props.total - props.attempted))

const milestones = computed(() => [
  { value: 25, label: '25%' },
  { value: 50, label: '50%' },
  { value: 75, label: '75%' },
  { value: 100, label: '100%' },
])

const getGradientColor = () => {
  const p = progressPercent.value
  if (p < 25) return 'linear-gradient(to right, #dc3545, #fd7e14)'
  if (p < 50) return 'linear-gradient(to right, #fd7e14, #ffc107)'
  if (p < 75) return 'linear-gradient(to right, #ffc107, #28a745)'
  return 'linear-gradient(to right, #28a745, #198754)'
}

const initChart = async () => {
  if (!props.showChart || !chartCanvas.value) return

  const { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } = await import(
    'chart.js'
  )
  Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

  const ctx = chartCanvas.value.getContext('2d')
  if (chartInstance) chartInstance.destroy()

  const barColor =
    progressPercent.value < 25
      ? '#dc3545'
      : progressPercent.value < 50
        ? '#fd7e14'
        : progressPercent.value < 75
          ? '#ffc107'
          : '#28a745'

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Completed', 'Remaining'],
      datasets: [
        {
          label: 'Quizzes',
          data: [props.attempted, remaining.value],
          backgroundColor: [barColor, '#e9ecef'],
          borderColor: [barColor, '#adb5bd'],
          borderWidth: 1,
          borderRadius: 6,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label(context) {
              const total = props.attempted + remaining.value
              const percentage = total > 0 ? Math.round((context.parsed.x / total) * 100) : 0
              return `${context.parsed.x} quizzes (${percentage}%)`
            },
          },
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          max: Math.max(props.total, 1),
        },
      },
      animation: {
        duration: props.animated ? 1000 : 0,
      },
    },
  })
}

onMounted(() => {
  nextTick(initChart)
})

watch([() => props.attempted, () => props.total], initChart)
</script>

<style scoped>
.dot-indicator {
  width: 12px;
  height: 12px;
  background-color: white;
  border: 2px solid #0d6efd;
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
}

.milestone-dot {
  width: 10px;
  height: 10px;
  background-color: #dee2e6;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}
</style>
