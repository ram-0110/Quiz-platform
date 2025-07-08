
<template>
  <div>
    <h1>About Page</h1>

    <div v-if="error" style="color: red">{{ error }}</div>

    <div v-else-if="aboutData">
      <pre>{{ aboutData }}</pre>
    </div>

    <div v-else>
      Loading...
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
const aboutData = ref(null);
const error = ref(null);

const token = localStorage.getItem('access_token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
} else {
  console.error('No token found in localStorage');
}


onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/about')
    aboutData.value = response.data
  } catch (err) {
    error.value = err.message || 'Failed to fetch data'
    console.error(err)
  }
})
</script>
