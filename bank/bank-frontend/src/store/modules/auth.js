import axios from 'axios'
import { API_BASE_URL, API_ENDPOINTS } from '@/config'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

const state = {
  user: null,
  token: localStorage.getItem('token') || ''
}

const mutations = {
  SET_USER(state, user) {
    state.user = user
  },
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
    // Set the token in axios default headers with Bearer prefix
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  },
  LOGOUT(state) {
    state.user = null
    state.token = ''
    localStorage.removeItem('token')
    // Remove the token from axios default headers
    delete api.defaults.headers.common['Authorization']
  }
}

const actions = {
  async register({ commit }, userData) {
    const response = await api.post(API_ENDPOINTS.AUTH.REGISTER, userData)
    commit('SET_USER', response.data.user)
    commit('SET_TOKEN', response.data.access)
    return response
  },
  
  async login({ commit }, credentials) {
    const response = await api.post(API_ENDPOINTS.AUTH.LOGIN, credentials)
    commit('SET_USER', response.data.user)
    commit('SET_TOKEN', response.data.access)
    return response
  },
  
  logout({ commit }) {
    commit('LOGOUT')
  },
  
  async fetchProfile({ commit }) {
    try {
      const response = await api.get(API_ENDPOINTS.AUTH.PROFILE)
      commit('SET_USER', response.data)
      return response
    } catch (error) {
      console.error('Failed to fetch profile:', error)
      throw error
    }
  }
}

const getters = {
  isAuthenticated: state => !!state.token,
  currentUser: state => state.user
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 