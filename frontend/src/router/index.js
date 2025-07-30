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
import result from '@/views/user/ResultPage.vue'
import admin_stats from '@/views/admin/admin_stats.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/quiz/result/:quizId',
      name: 'result',
      component: result,
      props: true,
    },
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
      meta: { isAdmin: true },
    },
    {
      path: '/admin/add-quiz',
      name: 'add-quiz',
      component: add_quiz,
      meta: { isAdmin: true },
    },
    {
      path: '/admin/edit_quiz/:id',
      name: 'edit-quiz',
      component: edit_quiz,
      meta: { isAdmin: true },
    },
    {
      path: '/admin/stats',
      name: 'admin-stats',
      component: admin_stats,
      meta: { isAdmin: true },
    }
  ],
})

router.beforeEach((to, from, next) => {
  const publicPages = ['login', 'signup']
  const token = localStorage.getItem('access_token')
  const username = localStorage.getItem('username')

  if (token && publicPages.includes(to.name)) {
    return next({ name: 'dashboard' })
  }

  if (!token && !publicPages.includes(to.name)) {
    return next({ name: 'login' })
  }

  if (to.meta.isAdmin && username !== 'admin') {
    return next({ name: 'dashboard' }) // or a 403 page
  }

  next()
})

export default router
