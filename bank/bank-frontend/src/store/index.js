import { createStore } from 'vuex'
import auth from './modules/auth'

export default createStore({
  state: {
    user: null,
    token: null
  },
  modules: {
    auth
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
    }
  },
  actions: {
    // Здесь будут ваши actions
  }
})