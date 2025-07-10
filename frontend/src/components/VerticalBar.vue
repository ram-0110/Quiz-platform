// Add this component to your project: VerticalBar.vue
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  label: String,
  scored: Number,
  total: Number,
})

const chartData = computed(() => ({
  labels: ['Attempted Quizzes'],
  datasets: [
    {
      label: 'Attempted',
      backgroundColor: '#4ade80',
      data: [props.scored],
    },
    {
      label: 'Total',
      backgroundColor: '#f87171',
      data: [props.total],
    },
  ],
}))

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: props.label,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
    },
  },
}
</script>
