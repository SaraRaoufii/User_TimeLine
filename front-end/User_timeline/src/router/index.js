import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../pages/auth/UserLogin.vue') },
  { path: '/', name: 'Dashboard', component: () => import('../pages/UserDashboard.vue'), meta: { requiresAuth: true } },
  { path: '/userpanel/:username', name: 'userpanel', component: () => import('../pages/users/UseerProfile.vue'), meta: { requiresAuth: true } },
  { path: '/userslistpage', name:'userslist', component:() => import('../pages/users/UsersListPage.vue'), meta: { requiresAuth: true } },
  { path: '/managelogs', name: 'managelogs', component: () => import('../pages/logs/ManageLogs.vue'), meta: { requiresAuth: true } },
  { path: '/authlogs', name: 'authlogs', component: () => import('../pages/logs/AuthLogs.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  if (to.name === 'Login') return next()

  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      await userStore.initUser()
    }

    if (userStore.isLoggedIn) {
      next()
    } else {
      next({ name: 'Login' })
    }
  } else {
    next()
  }
})

export default router
