<template>
  <div class="d-flex vh-100">
    <!-- Left Panel -->
    <div class="left-panel d-flex flex-column justify-content-between p-4 bg-light text-dark">
      <div class="logo fw-bold ms-2 mt-2">
        <img src="@/components/img/Logo.svg" alt="" width="75" height="40 " />
      </div>
    </div>

    <!-- Right Panel -->
    <div
      class="right-panel d-flex flex-column justify-content-center align-items-center bg-white text-dark px-4"
    >
      <div class="w-100" style="max-width: 400px">
        <h3 class="mb-2">Login</h3>
        <p class="text-muted mb-4">Enter your Login credentials below</p>
        <div class="mb-4 login-form-css"><Login_form /></div>

        <small class="d-block text-muted text-center mt-3">
          By clicking continue, you agree to our
          <a href="#" class="">Terms of Service</a> and <a href="#" class="">Privacy Policy</a>.
        </small>
      </div>
    </div>
  </div>
</template>

<script setup>
import Login_form from '@/components/Login_form.vue'
// No logic for now
</script>

<style scoped>
.left-panel {
  width: 50%;
  border-right: 1px solid #dee2e6;
}

.right-panel {
  width: 50%;
}
.login-form-css {
  align-items: center;
  margin-left: 2.2rem;
}

h3 {
  font-size: 2rem;
  font-weight: 400;
}
a {
  text-decoration: none;
  color: black;
}
h3 {
  font-size: 2rem;
  font-weight: 400;
  text-align: center;
}
p {
  font-size: 1rem;
  text-align: center;
}
</style>
