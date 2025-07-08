<template>
  <div class="login-container">
    <form class="login-form" @submit.prevent="handleSubmit">
      <input
        type="username"
        id="username"
        placeholder="Username"
        v-model="form.username"
        required
      />
      <input type="email" id="email" placeholder="name@example.com" v-model="form.email" required />
      <input
        type="password"
        id="password"
        placeholder="Password"
        v-model="form.password"
        required
      />
      <input
        type="password"
        id="confirm-password"
        placeholder="Confirm Password"
        v-model="form.confirmPassword"
        required
      />
      <button type="submit">Sign Up</button>
      <div>
        <p class="alt-link">
          Already have an account?
          <RouterLink to="/login" class="signup-link">Log in</RouterLink>
        </p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
const router = useRouter()
const toster = useToast()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/signup', form)
    console.log('Signup successful:', response.data)
    toster.success('Signup successful')
    router.push('/login')
  } catch (error) {
    toster.error('Invalid')
    console.error('Error during signup:', error)
  }
}
</script>

<style scoped>
.alt-link {
  font-size: 0.85rem;
  text-align: center;
  color: #666;
  margin-top: 1rem;
}

.signup-link {
  color: black;
  text-decoration: none;
  font-weight: 500;
}

.signup-link:hover {
  text-decoration: underline;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 320px;
}

.login-form input {
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.login-form input:focus {
  border-color: #333;
}

.login-form button {
  padding: 0.75rem 1rem;
  background-color: #222;
  color: #fff;
  font-weight: 500;
  font-size: 0.95rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-form button:hover {
  background-color: #000;
}
</style>
