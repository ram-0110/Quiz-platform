<template>
  <header class="header">
    <div>
      <h1 class="title">{{ props.title }}</h1>
      <p class="subtitle">{{ props.subtitle }}</p>
    </div>
  </header>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    default: 'Welcome back!',
  },
  subtitle: {
    type: String,
    default: "Here's a list of your tasks for this month!",
  },
})
</script>

<style scoped>
/* Header styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e2e2;
}

.title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
}

.subtitle {
  font-size: 0.875rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}
</style>
