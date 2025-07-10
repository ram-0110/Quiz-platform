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

// Normalize: (score / total_marks) * 100
const chartData = {
  labels: props.subjects.map((s) => s.subject_name),
  datasets: [
    {
      label: 'Subject Performance (%)',
      data: props.subjects.map((s) =>
        s.total_marks > 0 ? Math.round((s.scored / s.total_marks) * 100) : 0,
      ),
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 2,
      pointBackgroundColor: 'rgba(54, 162, 235, 1)',
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
      },
    },
  },
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Subject-wise Score %',
    },
  },
}
</script>
