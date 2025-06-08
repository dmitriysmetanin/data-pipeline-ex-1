<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label>Email</label>
        <input v-model="credentials.email" type="email" required>
      </div>
      <div>
        <label>Password</label>
        <input v-model="credentials.password" type="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>
<script>
export default {
  name: 'AuthLogin', // Изменено с 'Login'
  data() {
    return {
      credentials: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    async login() {
      try {
        await this.$store.dispatch('auth/login', this.credentials)
        this.$router.push('/profile')
      } catch (error) {
        console.error('Login failed:', error)
        // Добавьте уведомление для пользователя
      }
    }
  }
}
</script>