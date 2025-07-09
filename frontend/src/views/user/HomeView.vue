<template>
  <div class="dashboard-container">
    <PageHeader title="Explore!" subtitle="Add new Subjects" />
  </div>
</template>

<script setup>
import PageHeader from '@/components/PageHeader.vue'
</script>

<style scoped>
.dashboard-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #000;
  background-color: #fff;
  max-width: 92vw;
  margin: 0 auto;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e2e2;
  border-radius: 8px;
}

.subDir {
  border-bottom: 1px solid #e2e2e2;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
}

.add-subject-section {
  margin-bottom: 24px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: white;
}

.add-subject-form h4 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: black;
}

.form-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.form-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: black;
}

.add-btn {
  background: black;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

.add-btn:hover {
  background: #333;
}

.add-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.no-btn {
  background: none;
  border: none;
  font-size: inherit;
}

.subjects-container {
  border: 1px solid #e2e2e2;
  border-radius: 0.5rem;
  overflow: hidden;
  margin-top: 1rem;
  max-height: 40vh;
}

.accordion-item {
  border: none;
  border-bottom: 1px solid #e2e2e2;
}

.accordion-item:last-child {
  border-bottom: none;
}

.accordion-button {
  padding: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #333;
  background-color: #fff;
  box-shadow: none;
  border: none;
  width: 100%;
  text-align: left;
}

.accordion-button:not(.collapsed) {
  color: #000;
  background-color: #f8f8f8;
}

.accordion-button:focus {
  box-shadow: none;
  border-color: transparent;
}

.subject-header {
  display: flex;
  align-items: center;
  width: 100%;
}

.subject-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  margin-right: 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #666;
}

.subject-name {
  flex: 1;
  font-weight: 500;
}

.topic-count {
  margin-left: auto;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  background-color: #f5f5f5;
  color: #666;
}

.accordion-body {
  padding: 0;
}

.topic-list {
  border-top: 1px solid #e2e2e2;
}

.topic-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: background-color 150ms ease;
}

.topic-item:last-child {
  border-bottom: none;
}

.topic-item:hover {
  background-color: #f8f8f8;
}

.topic-content {
  display: flex;
  align-items: center;
  flex: 1;
}

.topic-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #666;
}

.topic-name {
  font-size: 0.875rem;
  color: #333;
}

.topic-arrow {
  font-size: 0.75rem;
  color: #999;
  opacity: 0;
  transition: opacity 150ms ease;
}

.topic-item:hover .topic-arrow {
  opacity: 1;
}
</style>
