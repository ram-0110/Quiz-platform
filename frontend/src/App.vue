<script setup>
import { RouterView, useRoute } from 'vue-router'
import Nav_bar from './components/Nav_bar.vue'

const route = useRoute()
</script>

<template>
  <div v-if="route.name !== 'login' && route.name !== 'signup'" class="bg-dark text-center">
    <Nav_bar />
  </div>
  <RouterView />
</template>
