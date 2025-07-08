import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/user/HomeView.vue'
import AboutView from '../views/user/AboutView.vue'
import DashboardView from '../views/user/DashboardView.vue'
import Quiz_page from '../views/user/Quiz_page.vue'
import Quiz_start from '../views/user/Quiz_start.vue'
import ststs_user from '@/views/user/ststs_user.vue'
import LoginPage from '@/views/user/LoginPage.vue'
import SignupPage from '@/views/user/SignupPage.vue'
import admin_dashbord from '@/views/admin/admin_dashbord.vue'
import add_quiz from '@/views/admin/add_quiz.vue'
import edit_quiz from '@/views/admin/edit_quiz.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/quiz/:quiz_id',
      name: 'quiz',
      component: Quiz_page,
      props: true,
    },
    {
      path: '/quiz/start/:quiz_id',
      name: 'quiz-start',
      component: Quiz_start,
      props: true,
    },
    {
      path: '/stats',
      name: 'stats',
      component: ststs_user,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupPage,
    },
    {
      path: '/admin',
      name: 'admin',
      component: admin_dashbord,
    },
    {
      path: '/admin/add-quiz',
      name: 'add-quiz',
      component: add_quiz,
    },
    {
      path: '/admin/edit_quiz/:id',
      name: 'edit-quiz',
      component: edit_quiz,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const publicPages = ['login', 'signup']
  const token = localStorage.getItem('access_token') // Use the correct key for your token

  if (token && publicPages.includes(to.name)) {
    // If logged in, redirect away from login/signup to dashboard
    return next({ name: 'dashboard' })
  }

  if (!token && !publicPages.includes(to.name)) {
    // Not logged in and trying to access protected page
    return next({ name: 'login' })
  }

  next()
})

export default router
