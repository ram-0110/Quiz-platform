<!-- quiz_page.vue -->
<template>
  <div class="container bg-white border rounded shadow-sm my-4 py-3 px-4">
    <div class="row">
      <div class="col-12 mb-3 text-center">
        <h2 class="fw-bold border-bottom pb-2">Optics Quiz-1</h2>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="quiz-details mb-3">
          <div class="detail-item d-flex align-items-center mb-1">
            <span class="detail-label fw-bold me-2">Instructor:</span>
            <span class="detail-value">Prof. Name</span>
          </div>
          <div class="detail-item d-flex align-items-center mb-1">
            <span class="detail-label fw-bold me-2">Date:</span>
            <span class="detail-value">19/03/2025</span>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="quiz-details mb-3">
          <div class="detail-item d-flex align-items-center mb-1">
            <span class="detail-label fw-bold me-2">Duration:</span>
            <span class="detail-value">10 minutes</span>
          </div>
          <div class="detail-item d-flex align-items-center mb-1">
            <span class="detail-label fw-bold me-2">Total Marks:</span>
            <span class="detail-value">50</span>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-2">
      <div class="col-12">
        <div class="quiz-instructions p-2 bg-light rounded">
          <p class="fw-light mb-1 small">Click on the button below to start the quiz.</p>
          <p class="fw-light mb-0 smaller-text">
            By starting, I agree to follow all instructions.
          </p>
        </div>
      </div>
    </div>

    <div class="row mt-3">
      <div class="col-12 text-center">
        <RouterLink to="/quiz/start" class="btn btn-dark btn-sm px-3 py-1"> Start Quiz </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.container {
  max-width: 700px;
}

h2 {
  font-size: 1.5rem;
  color: #212121;
  letter-spacing: 0.01em;
}

.quiz-details {
  font-size: 0.95rem;
}

.detail-label {
  min-width: 80px;
  font-size: 0.9rem;
}

.detail-value {
  font-weight: 400;
  font-size: 0.9rem;
}

.quiz-instructions {
  border-left: 3px solid #212529;
  font-size: 0.9rem;
}

.small {
  font-size: 0.9rem;
}

.smaller-text {
  font-size: 0.8rem;
  color: #666;
}

.btn-dark {
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-dark:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}

@media (max-width: 768px) {
  .container {
    padding: 1rem !important;
  }

  h2 {
    font-size: 1.3rem;
  }

  .detail-label {
    min-width: 70px;
  }
}
</style>
