<template>
  <div class="profile">
    <h2>User Profile</h2>
    <div v-if="user">
      <p><strong>Name:</strong> {{ user.first_name }} {{ user.last_name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p v-if="user.birth_date"><strong>Birth Date:</strong> {{ user.birth_date }}</p>
      <p v-if="user.phone_number"><strong>Phone:</strong> {{ user.phone_number }}</p>
      <p v-if="user.address"><strong>Address:</strong> {{ user.address }}</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    user() {
      return this.$store.getters['auth/currentUser']
    }
  },
  created() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      try {
        await this.$store.dispatch('auth/fetchProfile')
      } catch (error) {
        console.error('Failed to fetch profile:', error)
        this.$router.push('/login')
      }
    },
    logout() {
      this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  }
}
</script>