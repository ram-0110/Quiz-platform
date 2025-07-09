<template>
  <div class="login-container">
    <form class="login-form" @submit.prevent="handleSubmit">
      <input type="email" id="email" placeholder="name@example.com" v-model="form.email" required />
      <input
        type="password"
        id="password"
        placeholder="Password"
        v-model="form.password"
        required
      />
      <button type="submit">Log In</button>
      <div>
        <p class="alt-link">
          Don't have an account?
          <RouterLink to="/signup" class="signup-link">Sign up instead</RouterLink>
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
const toast = useToast()

const form = reactive({
  email: '',
  password: '',
})

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/login', form)
    console.log('Login successful:', response.data)

    const accessToken = response.data.access_token
    const refreshToken = response.data.refresh_token
    const username = response.data.username

    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
    localStorage.setItem('username', username) // ✅ store this

    toast.success('Login successful!')

    if (username === 'admin') {
      router.push('/admin') // ✅ Go to admin dashboard
    } else {
      router.push('/dashboard') // ✅ Regular user
    }

  } catch (error) {
    console.error('Error during login:', error)
    toast.error('Invalid email or password')
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
