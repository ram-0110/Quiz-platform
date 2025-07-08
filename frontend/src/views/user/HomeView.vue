<template>
  <h1 class="m-5 p-5">Home</h1>
  <div class="m-5 p-5">
    <h1 v-if="message">{{ message }}</h1>
    <p v-else>Loading...</p>
    </div>
</template>

<script setup>
import api from '@/axios/axios';
import { ref, onMounted } from 'vue';
const message = ref(null)

onMounted(async () => {
  try {
    const response = await api.get('/home');
    message.value = response.data.message;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});
</script>
