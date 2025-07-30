<template>
  <nav v-if="showNavbar" class="navbar navbar-expand-lg bg-white">
    <div class="container-fluid">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarTogglerDemo01"
        aria-controls="navbarTogglerDemo01"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
        <a class="navbar-brand mx-5" href="#">
          <img src="../components/img/Logo.svg" alt="" width="75" height="40" />
        </a>

        <ul v-if="isAdmin" class="navbar-nav me-auto mb-2 mb-lg-0 mx-5">
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" :class="{ active: route.path === '/admin' }" to="/admin">
              Dashboard
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link"
              :class="{ active: route.path === '/admin/stats' }"
              to="/admin/stats"
            >
              Stats
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <button class="nav-link" @click="logout">Logout</button>
          </li>
        </ul>

        <ul v-else class="navbar-nav me-auto mb-2 mb-lg-0 mx-5">
          <li class="nav-item mx-2">
            <RouterLink
              class="nav-link"
              :class="{ active: route.path === '/dashboard' }"
              to="/dashboard"
            >
              Dashboard
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" :class="{ active: route.path === '/' }" to="/">
              Home
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" :class="{ active: route.path === '/stats' }" to="/stats">
              Stats
            </RouterLink>
          </li>
          <li class="nav-item mx-2">
            <button class="nav-link" @click="logout">Logout</button>
          </li>
        </ul>

        <form class="d-flex mx-5" role="search">
          <input
            class="form-control me-2 rounded-pill"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
        </form>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { ref, onMounted, computed } from 'vue'

const router = useRouter()
const route = useRoute()

const isAdmin = ref(false)

onMounted(() => {
  const username = localStorage.getItem('username')
  isAdmin.value = username === 'admin'
})

const showNavbar = computed(() => {
  return !route.path.startsWith('/quiz/start')
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('username')
  localStorage.removeItem('quiz_start_time')
  localStorage.removeItem('quiz_duration')
  router.push('/login')
}
</script>
