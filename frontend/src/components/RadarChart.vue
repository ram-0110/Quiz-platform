<!-- RadarChart.vue -->
<template>
  <Radar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Radar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, RadialLinearScale, PointElement, LineElement, Filler)

const props = defineProps({
  subjects: {
    type: Array,
    required: true,
  },
})

const chartData = {
  labels: props.subjects.map((s) => s.subject_name),
  datasets: [
    {
      label: 'Subject Performance (%)',
      data: props.subjects.map((s) =>
        s.total_marks > 0 ? Math.round((s.scored / s.total_marks) * 100) : 0,
      ),
      backgroundColor: 'rgba(207, 226, 255, 0.5)', // light blue
      borderColor: '#9ec5fe',
      pointBackgroundColor: '#6ea8fe',
    },
  ],
}

const chartOptions = {
  responsive: true,
  scales: {
    r: {
      suggestedMin: 0,
      suggestedMax: 100,
      ticks: {
        stepSize: 20,
        backdropColor: 'transparent',
        color: '#333333',
      },
      grid: {
        color: 'rgba(0,0,0,0.1)',
      },
      angleLines: {
        color: 'rgba(0,0,0,0.1)',
      },
      pointLabels: {
        color: '#333333',
      },
    },
  },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: '#333333',
      },
    },
    title: {
      display: true,
      text: 'Subject-wise Score %',
      color: '#333333',
    },
  },
}
</script>
