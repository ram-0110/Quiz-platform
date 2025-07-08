<template>
  <div class="subject-selector">
    <div class="header">
      <div>
        <h2 class="title">Quiz</h2>
        <p class="subtitle">Browse available quizzes</p>
      </div>

      <div class="action-container">
        <RouterLink class="add-button text-decoration-none" to="/admin/add-quiz">
          <i class="bi bi-plus me-2"></i>Add New Quiz
        </RouterLink>
      </div>
    </div>

    <div class="search-container mb-3">
      <input
        type="text"
        placeholder="Filter Quizzes..."
        class="search-input"
        v-model="searchQuery"
      />
    </div>

    <div class="table-container">
      <table class="task-table">
        <thead>
          <tr>
            <th>Quiz ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Time</th>
            <th>Update</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in filteredTasks" :key="task.id" class="task-row">
            <td>{{ task.id }}</td>
            <td>
              <span class="task-badge" :class="getBadgeClass(task.type)">{{ task.type }}</span>
              <span class="task-description">{{ task.description }}</span>
            </td>
            <td>
              <div class="status-indicator" :class="getStatusClass(task.status)">
                <span>{{ task.status }}min</span>
              </div>
            </td>
            <td>
              <div class="priority-indicator" :class="getPriorityClass(task.priority)">
                <span>{{ task.priority }}</span>
              </div>
            </td>
            <td>
              <RouterLink :to="`/admin/edit_quiz/${task.id}`" class="text-action update-action">
                <i class="bi bi-pencil me-1"></i>Update
              </RouterLink>
            </td>
            <td>
              <span class="text-action delete-action" @click="deleteTask(task)">
                <i class="bi bi-trash me-1"></i>Delete
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/axios/axios'

const props = defineProps({
  chapter: {
    type: String,
    required: true,
  },
})

const tasks = ref([])
const searchQuery = ref('')

// Fetch quizzes from API
const fetchData = async (chapter) => {
  try {
    const response = await api.get('/get-quiz-admin', { params: { chapter } })
    tasks.value = response.data
  } catch (error) {
    console.error('Error fetching tasks:', error)
  }
}

onMounted(() => {
  fetchData(props.chapter)
})

watch(
  () => props.chapter,
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      fetchData(newVal)
    }
  },
)

const filteredTasks = computed(() => {
  if (!searchQuery.value) return tasks.value

  const query = searchQuery.value.toLowerCase()
  return tasks.value.filter((task) =>
    [task.id, task.description, task.status, task.priority, task.type].some((field) =>
      field?.toLowerCase().includes(query),
    ),
  )
})

// Helper functions
const getBadgeClass = (type) => {
  return (
    {
      Documentation: 'badge-documentation',
      Bug: 'badge-bug',
      Feature: 'badge-feature',
    }[type] || ''
  )
}

const getStatusClass = (status) => {
  return (
    {
      'In Progress': 'status-in-progress',
      Backlog: 'status-backlog',
      Todo: 'status-todo',
      Done: 'status-done',
      Canceled: 'status-canceled',
    }[status] || ''
  )
}

const getPriorityClass = (priority) => {
  return (
    {
      High: 'priority-high',
      Medium: 'priority-medium',
      Low: 'priority-low',
    }[priority] || ''
  )
}
</script>

<style scoped>
.text-action {
  font-size: 0.85rem;
  color: #6c757d; /* Bootstrap muted */
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: color 0.2s;
}

.text-action i {
  font-size: 0.9rem;
}

.text-action:hover {
  color: #000; /* Darker on hover */
  text-decoration: underline;
}

.update-action i {
  color: #0d6efd;
}
.update-action {
  color: #0d6efd;
  text-decoration: none;
}

.delete-action i {
  color: #dc3545;
}
.delete-action {
  color: #dc3545;
}
.subject-selector {
  margin-bottom: 2rem;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  padding: 1.5rem;
  background-color: #fff;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e2e2e2;
  padding-bottom: 1rem;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
}

.subtitle {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.25rem;
}

.add-button {
  display: inline-flex;
  align-items: center;
  height: 2.5rem;
  padding: 0 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  background-color: #000;
  border-radius: 0.375rem;
  transition: background-color 150ms ease;
}

.add-button:hover {
  background-color: #333;
}

.search-container {
  max-width: 300px;
}

.search-input {
  width: 100%;
  height: 2.5rem;
  padding: 0 0.75rem;
  font-size: 0.875rem;
  border: 1px solid #e2e2e2;
  border-radius: 0.375rem;
}

.search-input:focus {
  outline: none;
  border-color: #999;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.05);
}

.table-container {
  overflow-x: auto;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
}

.task-table th,
.task-table td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  text-align: left;
  border-bottom: 1px solid #e2e2e2;
}

.task-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  text-transform: uppercase;
  color: #666;
}

.task-row:hover {
  background-color: #f8f8f8;
}

.task-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  background-color: #f5f5f5;
  border: 1px solid #e2e2e2;
  margin-right: 0.5rem;
}

.task-description {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400px;
  display: inline-block;
  vertical-align: middle;
}

.status-indicator,
.priority-indicator {
  display: inline-flex;
  align-items: center;
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background-color: #f5f5f5;
  border: 1px solid #e2e2e2;
}

@media (max-width: 768px) {
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
