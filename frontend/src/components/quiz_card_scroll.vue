<template>
  <RouterLink :to="`/quiz/${props.item.quiz_id}`" class="card-link">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ quiz_name }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">Time:{{ quiz_time }}</h6>
        <p class="card-text">
          <small class="text-muted">Date: {{ quiz_date }}</small>
        </p>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
import api from '@/axios/axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

const quiz_name = ref('')
const quiz_date = ref('')
const quiz_time = ref('')

const props = defineProps({
  item: Object,
})

onMounted(async () => {
  try {
    const response = await api.get('/dashboard-cardnum', {
      params: { id: props.item.quiz_id },
    })
    const data = response.data

    quiz_name.value = data.quiz_data.quiz_name
    quiz_date.value = data.quiz_data.date_of_quiz
    quiz_time.value = data.quiz_data.time_duration

    console.log(data.quiz_data)
    console.log('Fetched data:', data.message)
  } catch (error) {
    console.error('Error fetching card data:', error)
    toast.error('Failed to load quiz data') 
  }
})
</script>

<style scoped>
.card-link {
  text-decoration: none;
  color: inherit;
  display: inline-block;
  margin: 0.75rem;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.card {
  cursor: pointer;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  padding: 0.5rem;
  width: 20rem;
}
.card-title {
  font-size: 1.25rem;
  font-weight: 400;
  margin: 0.5rem 0;
  color: #333;
}

.card-subtitle {
  font-size: 0.8rem;
}

.text-muted {
  color: #6c757d;
}

.card-text {
  margin-bottom: 0.75rem;
}

.card-text:last-child {
  margin-bottom: 0;
}

.card-text strong {
  font-weight: 600;
}

/* Hover animation */
.card-link:hover {
  transform: translateY(-3px);
}

.card-link:hover .card {
  border-color: #d0d0d0;
  background-color: #fdfdfd;
}
</style>
