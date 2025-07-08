
<template>
  <nav class="navbar navbar-expand-lg bg-white">
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
          <img src="../components/img/Logo.svg" alt="" width="75" height="40 " />
        </a>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0 mx-5">
          <li class="nav-item mx-2">
            <RouterLink class="nav-link active" aria-current="page" to="/dashboard"
              >Dashboard</RouterLink
            >
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" to="/">Home</RouterLink>
          </li>
          <li class="nav-item mx-2">
            <RouterLink class="nav-link" aria-disabled="true" to="/stats">Stats</RouterLink>
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
import { useRouter,RouterLink } from 'vue-router'
const router = useRouter()

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}
</script>
