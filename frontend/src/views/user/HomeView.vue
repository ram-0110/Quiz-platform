<template>
  <div class="dashboard-container">
    <PageHeader title="Explore!" subtitle="Add new Subjects" />

    <div class="subDir">
      <!-- Add Subject Form -->
      <div class="add-subject-section">
        <div class="add-subject-form">
          <h4>Add New Subject</h4>
          <div class="form-group">
            <input
              v-model="newSubjectName"
              type="text"
              placeholder="Subject name"
              class="form-input"
            />
            <button @click="addNewSubject" class="add-btn">Add Subject</button>
          </div>
        </div>
      </div>
    </div>

    <div class="subDir">
      <div class="subjects-container overflow-auto">
        <div class="accordion" id="subjectsAccordion">
          <div class="accordion-item" v-for="(subject, index) in subjects" :key="subject.name">
            <h3 class="accordion-header" :id="'heading' + index">
              <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="'#collapse' + index"
                aria-expanded="false"
                :aria-controls="'collapse' + index"
              >
                <div class="subject-header">
                  <span class="subject-index">{{ index + 1 }}</span>
                  <span class="subject-name">{{ subject.name }}</span>
                  <span class="topic-count">{{ subject.topics.length }} topics</span>
                </div>
              </button>
            </h3>
            <div
              :id="'collapse' + index"
              class="accordion-collapse collapse"
              :aria-labelledby="'heading' + index"
              data-bs-parent="#subjectsAccordion"
            >
              <div class="accordion-body">
                <div class="topic-list">
                  <div class="topic-item" v-for="(topic, i) in subject.topics" :key="i">
                    <div class="topic-content">
                      <span class="topic-index">{{ index + 1 }}.{{ i + 1 }}</span>
                      <button @click="setActiveSubject(topic)" class="no-btn">
                        <span class="topic-name">{{ topic }}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PageHeader from '@/components/PageHeader.vue'

import api from '@/axios/axios'
import { ref, onMounted } from 'vue'
const message = ref(null)
const subjects = ref(null)
const newSubjectName = ref('')

const addNewSubject = async () => {
  console.log(newSubjectName.value)
  const response = await api.post('/add-stu-sub', { name: newSubjectName.value })
  console.log(response)
}

onMounted(async () => {
  try {
    const response = await api.get('/home')
    message.value = response.data.message
    subjects.value = response.data.unopted_subjects
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})
</script>

<style scoped>
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
.login-form {
  max-height: 5vh;
}
.login-form input {
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 0.2s ease;
}
.no-btn {
  background: none;
  border: none;
  font-size: inherit;
}
.minimal-form {
  background-color: #fff;
  color: #000;
  max-width: 20vw;
}

/* Inputs */
n.minimal-input {
  background-color: transparent;
  border: 1px solid #000;
  color: #000;
  border-radius: 0.25rem;
  padding: 0.5rem 0.75rem;
}
.minimal-input::placeholder {
  color: #666;
  font-style: italic;
}
.minimal-input:focus {
  box-shadow: none;
  border-color: #000;
}

/* Button */
.minimal-btn {
  background-color: #000;
  border: 1px solid #000;
  color: #ffffff;
  border-radius: 0.25rem;

  transition:
    background-color 0.2s ease,
    color 0.2s ease;

  margin-left: auto;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
}

.minimal-btn:hover,
.minimal-btn:focus {
  background-color: #242424;
  color: #ffffff;
  box-shadow: none;
}
/* Container */
.subject-selector {
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  background-color: #fff;
  margin-bottom: 2rem;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e2e2;
}

.header-1 {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
}

.subtitle {
  font-size: 0.875rem;
  color: #666;
  margin: 0.25rem 0 0 0;
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

/* Search */
.search-container {
  flex: 1;
  max-width: 300px;
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

/* Subjects Accordion */
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

/* Topics */
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
  text-decoration: none;
  background: none;
  padding-right: 90vw;
  border: none;
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
.subDir {
  border-bottom: 1px solid #e2e2e2;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
}
/* Base styles */
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

.quiz-title {
  border-top: 1px solid #e2e2e2;

  font-size: 1.5rem;
  font-weight: 600;
  margin: 1.5rem 0 1rem;
}

/* Subject selector styles */
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

/* Topic list */
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

/* Controls */
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

/* Table styles */
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

/* Responsive adjustments */
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
