<template>
  <div class="max-w-4xl mx-auto p-6 space-y-12">
    <h2 class="text-2xl font-bold text-center mb-6">Your Quiz Stats</h2>

    <div v-for="(chart, index) in charts" :key="index">
      <h3 class="text-lg font-semibold text-center mb-2">{{ chart.title }}</h3>

      <!-- Always render canvas -->
      <canvas :ref="chart.ref" class="w-full max-h-[400px]"></canvas>

      <!-- Show fallback only if all scores are zero -->
      <p
        v-if="chart.data.scores.length && chart.data.scores.every((score) => score === 0)"
        class="text-center text-gray-500"
      >
        No meaningful data to display
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import api from '@/axios/axios'

// Refs for canvas elements
const subjectRef = ref(null)
const chapterRef = ref(null)
const quizRef = ref(null)

// Chart configuration array
const charts = [
  {
    title: 'Subject-wise Score',
    ref: subjectRef,
    data: { labels: [], scores: [] },
    key: 'subject',
  },
  {
    title: 'Chapter-wise Score (Subject ID: 1)',
    ref: chapterRef,
    data: { labels: [], scores: [] },
    key: 'chapter',
  },
  {
    title: 'Quiz-wise Score (Chapter ID: 1)',
    ref: quizRef,
    data: { labels: [], scores: [] },
    key: 'quiz',
  },
]

const renderChart = (canvas, labels, scores, title) => {
  new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Score',
          data: scores,
          backgroundColor: '#4F46E5',
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: title,
        },
      },
    },
  })
}

onMounted(async () => {
  try {
    const res = await api.get(`/stats/static`)
    console.log('Stats response:', res.data)

    await nextTick() // Ensure canvas elements exist

    charts.forEach((chart) => {
      const chartData = res.data?.[chart.key] ?? []

      chart.data.labels = chartData.map((d) => d.label)
      chart.data.scores = chartData.map((d) => d.score)

      if (chart.ref.value) {
        renderChart(chart.ref.value, chart.data.labels, chart.data.scores, chart.title)
      } else {
        console.warn(`Chart ref for ${chart.key} not ready.`)
      }
    })
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
})
</script>
