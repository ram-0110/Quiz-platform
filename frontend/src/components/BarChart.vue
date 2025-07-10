<template>
  <div class="chart-wrapper">
    <div class="chart-container">
      <canvas ref="canvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Chart, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js'

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
  quizData: {
    type: Array,
    required: true,
  },
})

const canvas = ref(null)
let chartInstance = null

const renderChart = () => {
  if (!canvas.value) return

  const labels = props.quizData.map((q) => q.quiz_name)
  const scores = props.quizData.map((q) => q.score)

  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(canvas.value.getContext('2d'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Score %',
          data: scores,
          backgroundColor: '#9ec5fe', // use a visible color on white theme
          borderRadius: 8,
          barThickness: 40,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            color: '#333333', // dark gray x-axis labels
          },
          grid: {
            color: 'rgba(0,0,0,0.05)', // light gray x-axis grid
          },
        },
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            color: '#333333', // dark gray y-axis labels
          },
          grid: {
            color: 'rgba(0,0,0,0.05)', // light gray y-axis grid
          },
        },
      },
      plugins: {
        legend: {
          labels: {
            color: '#333333', // dark gray legend
          },
        },
        tooltip: {
          backgroundColor: '#333333',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
        },
      },
    },
  })
}

onMounted(() => {
  renderChart()
})

watch(
  () => props.quizData,
  () => {
    renderChart()
  },
  { deep: true },
)
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.chart-container {
  width: 100%;
  max-width: 1000px;
  height: 400px;
  background: #ffffff; /* ✅ Set to white for your theme */
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
