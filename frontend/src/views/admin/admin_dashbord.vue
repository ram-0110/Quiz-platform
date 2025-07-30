<!-- admin_dashboard.vue -->

<template>
  <div class="dashboard-container">
    <PageHeader title="Welcome back Admin!" subtitle="Manage your subjects and quizzes" />

    <div class="subDir">
      <SubjectDirectory @setActiveSubject="activeSubject" />
    </div>
    <div>
      <QuizDirectory :chapter="activeSubjects_list" />
    </div>
  </div>
</template>

<script setup>
import PageHeader from '@/components/PageHeader.vue'
import SubjectDirectory from '@/components/admin/SubjectDirectory.vue'
import QuizDirectory from '@/components/admin/QuizDirectory.vue'
import { ref } from 'vue'
const activeSubjects_list = ref('')
const activeSubject = (subject) => {
  activeSubjects_list.value = subject
}
</script>

<style scoped>
.subDir {
  border-bottom: 1px solid #e2e2e2;
  margin-bottom: 2rem;
}
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

.quiz-title {
  border-top: 1px solid #e2e2e2;

  font-size: 1.5rem;
  font-weight: 600;
  margin: 1.5rem 0 1rem;
}

.subject-selector {
  margin-bottom: 2rem;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  padding: 1.5rem;
  background-color: #fff;
}

.subject-selector .header {
  border-bottom: 1px solid #e2e2e2;
  margin-bottom: 1rem;
}

.subject-selector .title {
  font-size: 1.25rem;
}

.action-container {
  display: flex;
  justify-content: flex-end;
}

.add-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 2.5rem;
  padding: 0 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  background-color: #000;
  border: none;
  border-radius: 0.375rem;
  transition: background-color 150ms ease;
}

.add-button:hover {
  background-color: #333;
}

.search-wrapper {
  position: relative;
  max-width: 100%;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  font-size: 0.875rem;
}

.search-input {
  width: 100%;
  height: 2.5rem;
  padding: 0 0.75rem 0 2.25rem;
  font-size: 0.875rem;
  border: 1px solid #e2e2e2;
  border-radius: 0.375rem;
  background-color: #fff;
  transition: all 150ms ease;
}

.search-input:focus {
  outline: none;
  border-color: #999;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.05);
}

.search-input::placeholder {
  color: #999;
}

.subjects-container {
  border: 1px solid #e2e2e2;
  border-radius: 0.5rem;
  overflow: hidden;
  margin-top: 1rem;
}

/* Accordion styles */
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
  box-shadow: none;
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

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.75rem 0;
}

.search-container {
  flex: 1;
  max-width: 300px;
}

.table-container {
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  overflow-x: auto;
  overflow-y: visible; /* ✅ allow dropdown to be fully visible */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  max-height: unset; /* ✅ disable height clipping */
}

.task-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: left;
}

.task-table th {
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #666;
  padding: 0.75rem 1rem;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e2e2e2;
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.task-row {
  border-bottom: 1px solid #e2e2e2;
  transition: background-color 0.2s;
}

.task-row:hover {
  background-color: #f8f8f8;
}

.task-row:last-child {
  border-bottom: none;
}

.task-table td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  vertical-align: middle;
  border-bottom: 1px solid #e2e2e2;
}

.task-id {
  color: #666;
  font-weight: 500;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.task-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  background-color: #f5f5f5;
  white-space: nowrap;
  border: 1px solid #e2e2e2;
}

.badge-documentation,
.badge-bug,
.badge-feature {
  background-color: #f5f5f5;
  color: #333;
}

.task-description {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400px;
}

.status-column,
.priority-column {
  width: 150px;
}

.status-indicator,
.priority-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  border: 1px solid #e2e2e2;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.status-in-progress,
.status-backlog,
.status-todo,
.status-done,
.status-canceled {
  background-color: #f5f5f5;
}

.priority-high,
.priority-medium,
.priority-low {
  background-color: #f5f5f5;
}

.actions-column {
  width: 50px;
  text-align: center;
}

.action-button {
  background: transparent;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #f0f0f0;
}

.dots {
  font-size: 1.25rem;
  line-height: 1;
  color: #666;
}

@media (max-width: 768px) {
  .controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .search-container {
    max-width: 100%;
    width: 100%;
  }

  .task-description {
    max-width: 200px;
  }
}

@media (max-width: 640px) {
  .task-table th:nth-child(4),
  .task-table td:nth-child(4) {
    display: none;
  }

  .task-description {
    max-width: 150px;
  }
}
</style>
