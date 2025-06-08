import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from '../store'
import TransferPage from '@/views/TransferPage.vue'
import TransferBetweenOwnAccounts from '../views/TransferBetweenOwnAccounts.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/Auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/Auth/Register.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    // component: ProfileView,
    component: () => import('../components/Profile/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/catalog',
    name: 'Catalog',
    component: () => import('@/components/Catalog.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/accounts',
    name: 'Accounts',
    component: () => import('@/components/AccountsList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/accounts/open',
    name: 'OpenAccount',
    component: () => import('@/components/OpenAccount.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/accounts/:id',
    name: 'AccountDetail',
    component: () => import('@/components/AccountDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/payments',
    name: 'Payments',
    component: () => import('@/views/PaymentsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/payments/transfer',
    name: 'Transfer',
    component: TransferPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/transfer-between-own',
    name: 'TransferBetweenOwnAccounts',
    component: TransferBetweenOwnAccounts
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Глобальный guard для защиты приватных маршрутов
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters['auth/isAuthenticated']) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router