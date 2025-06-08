<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div>
        <label>First Name</label>
        <input v-model="user.first_name" type="text" required>
      </div>
      <div>
        <label>Last Name</label>
        <input v-model="user.last_name" type="text" required>
      </div>
      <div>
        <label>Email</label>
        <input v-model="user.email" type="email" required>
      </div>
      <div>
        <label>Password</label>
        <input v-model="user.password" type="password" required>
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <button type="submit" :disabled="loading">{{ loading ? 'Registering...' : 'Register' }}</button>
    </form>
  </div>
</template>

<script>
export default {
    name: 'AuthRegister',
  data() {
    return {
      user: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        birth_date: null,
        tax_id: '',
        phone_number: '',
        address: ''
      },
      error: '',
      loading: false
    }
  },
  methods: {
    async register() {
      this.error = ''
      this.loading = true
      try {
        await this.$store.dispatch('auth/register', this.user)
        this.$router.push('/profile')
      } catch (error) {
        if (error.response && error.response.data) {
          const errorData = error.response.data
          if (typeof errorData === 'object') {
            // Обработка ошибок в виде объекта
            const errorMessages = Object.entries(errorData).map(([field, messages]) => {
              if (Array.isArray(messages)) {
                return `${field}: ${messages.join(', ')}`
              } else if (typeof messages === 'string') {
                return `${field}: ${messages}`
              } else if (typeof messages === 'object') {
                return `${field}: ${Object.values(messages).join(', ')}`
              }
              return `${field}: ${messages}`
            })
            this.error = errorMessages.join('\n')
          } else if (typeof errorData === 'string') {
            // Если ошибка в виде строки
            this.error = errorData
          } else {
            this.error = 'Registration failed. Please try again.'
          }
        } else {
          this.error = 'Registration failed. Please try again.'
        }
        console.error('Registration failed:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}

button {
  padding: 10px;
  background-color: #00a86b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
  white-space: pre-line;
}
</style>