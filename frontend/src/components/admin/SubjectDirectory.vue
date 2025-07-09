<template>
  <div class="subject-selector">
    <div class="header">
      <div>
        <h2 class="title">Subject Directory</h2>
        <p class="subtitle">Browse available subjects and topics</p>
      </div>
      <div class="dropdown">
        <div class="action-container">
          <button
            class="add-button"
            data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasBottom"
            aria-controls="offcanvasBottom"
          >
            <i class="bi bi-plus me-2"></i>Add New Subject
          </button>

          <button
            class="add-button ms-2"
            data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasBottom-1"
            aria-controls="offcanvasBottom"
          >
            <i class="bi bi-plus me-2"></i>Add New Chapter
          </button>
        </div>
      </div>
    </div>

    <div class="search-container">
      <div class="search-wrapper">
        <i class="bi bi-search search-icon"></i>
        <input
          type="text"
          placeholder="Search subjects..."
          class="search-input"
          v-model="subjectSearchQuery"
        />
      </div>
    </div>

    <div class="subjects-container overflow-auto">
      <div class="accordion" id="subjectsAccordion">
        <div
          class="accordion-item"
          v-for="(subject, index) in filteredSubjects"
          :key="subject.name"
        >
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
                  <i class="bi bi-chevron-right topic-arrow"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="offcanvas offcanvas-bottom"
      tabindex="-1"
      id="offcanvasBottom"
      aria-labelledby="offcanvasBottomLabel"
    >
      <div class="offcanvas-header header-1">
        <h2 class="title">Add subject</h2>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>

      <div class="offcanvas-body small minimal-form p-4">
        <form class="login-form d-flex flex-column" @submit="handleSubmit">
          <label for="subjectName" class="form-label subtitle m-1">Subject Name</label>
          <input
            type="text"
            id="subjectName"
            class="form-control minimal-input mb-3"
            placeholder="Subject Name"
            v-model="form.subjectName"
            required
          />

          <button type="submit" class="btn minimal-btn align-self-start">Add Subject</button>
        </form>
      </div>
    </div>

    <div
      class="offcanvas offcanvas-bottom"
      tabindex="-1"
      id="offcanvasBottom-1"
      aria-labelledby="offcanvasBottomLabel"
    >
      <div class="offcanvas-header header-1">
        <h2 class="title">Add subject</h2>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>

      <div class="offcanvas-body small minimal-form p-4">
        <form class="login-form-2 d-flex flex-column" @submit="add_chapter">
          <label for="subjectName" class="form-label subtitle m-1">Subject Name</label>
          <input
            type="text"
            id="subjectName"
            class="form-control minimal-input mb-3"
            placeholder="Subject Name"
            v-model="add_chap_form.subjectName"
            required
          />
          <label for="chapterName" class="form-label subtitle m-1">Chapter Name</label>
          <input
            type="text"
            id="chapterName"
            class="form-control minimal-input mb-3"
            placeholder="Chapter Name"
            v-model="add_chap_form.chapterName"
            required
          />

          <button type="submit" class="btn minimal-btn align-self-start">Add Subject</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import api from '@/axios/axios'

const emit = defineEmits(['setActiveSubject'])
const active_subject = ref('')
const setActiveSubject = (subject) => {
  active_subject.value = subject
}
watch(active_subject, (newValue) => {
  emit('setActiveSubject', newValue)
})

const form = ref({
  subjectName: '',
})

const add_chap_form = reactive({
  subjectName: '',
  chapterName: '',
})

let subjects = ref([])

const subjectSearchQuery = ref('')

const handleSubmit = async () => {
  try {
    const response = await api.post('/add-subject', {
      subjectName: form.value.subjectName,
    })
    console.log('Subject added:', response.data.message)
  } catch (error) {
    console.error('Error adding subject:', error)
  }
}

const add_chapter = async () => {
  console.log(add_chap_form)

  try {
    const response = await api.post('/add-chapter', {
      subjectName: add_chap_form.subjectName,
      chapterName: add_chap_form.chapterName,
    })
    console.log('Chapter added:', response.data.message)
  } catch (error) {
    console.error('Error adding chapter:', error)
  }
}

const filteredSubjects = computed(() => {
  if (!subjectSearchQuery.value) return subjects.value

  const query = subjectSearchQuery.value.toLowerCase()
  console.log(query)
  return subjects.value.filter((subject) => {
    return (
      subject.name.toLowerCase().includes(query) ||
      subject.topics.some((topic) => topic.toLowerCase().includes(query))
    )
  })
})

onMounted(async () => {
  try {
    const response = await api.get('/subjects-chapters-admin')
    subjects.value = response.data.subjects
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})
</script>
<style scoped>
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

.minimal-input {
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

.minimal-btn {
  background-color: #000;
  border: 1px solid #000;
  color: #ffffff;
  border-radius: 0.25rem;
  padding: 0.4rem 1.8rem;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  font-size: 0.875rem;
}
.minimal-btn:hover,
.minimal-btn:focus {
  background-color: #242424;
  color: #ffffff;
  box-shadow: none;
}

.subject-selector {
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  background-color: #fff;
  margin-bottom: 2rem;
}

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
  text-decoration: none;
  background: none;
  padding-right: 70vw;
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
</style>
