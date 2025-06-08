<template>
  <div id="app">
    <div class="app-header">
      <div class="logo">e-банк</div>
      <div class="quotes-bar-header">
        <span v-for="q in quotes" :key="q.currency" class="quote">
          {{ q.currency }}: {{ q.value }}
        </span>
      </div>
      <input class="search-bar" placeholder="Поиск" />
      <router-link to="/catalog" class="catalog-icon-header" title="Каталог">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="3" width="7" height="7" rx="2" fill="#2c3e50"/>
          <rect x="14" y="3" width="7" height="7" rx="2" fill="#2c3e50"/>
          <rect x="3" y="14" width="7" height="7" rx="2" fill="#2c3e50"/>
          <rect x="14" y="14" width="7" height="7" rx="2" fill="#2c3e50"/>
        </svg>
      </router-link>
      <div class="user-info">
        <span v-if="currentUser">{{ currentUser.first_name }}</span>
        <svg style="vertical-align: middle; margin-left: 8px;" width="28" height="28" fill="#bbb"><circle cx="14" cy="14" r="12"/></svg>
        <button class="logout-btn" @click="logout" title="Выйти">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 17l5-5-5-5M21 12H9" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13 5v-2a2 2 0 0 0-2-2h-6a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-2" stroke="#bbb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
    <div class="app-layout">
      <aside class="side-nav">
        <nav>
          <router-link to="/" exact-active-class="active"><span class="icon-nav">🏠</span> Главный</router-link>
          <router-link to="/savings"><span class="icon-nav">💰</span> Накопления</router-link>
          <router-link to="/payments" active-class="active"><span class="icon-nav">💸</span> Платежи</router-link>
          <router-link to="/history"><span class="icon-nav">📜</span> История</router-link>
        </nav>
      </aside>
      <main class="main-content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      quotes: []
    }
  },
  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'currentUser'])
  },
  methods: {
    async logout() {
      await this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  },
  async mounted() {
    try {
      const res = await axios.get('http://localhost:8000/api/quotes/');
      this.quotes = res.data;
    } catch (e) {
      this.quotes = [];
    }
    const token = localStorage.getItem('token')
    if (token) {
      this.$store.commit('auth/SET_TOKEN', token)
      this.$store.dispatch('auth/fetchProfile').catch(() => {
        this.$store.dispatch('auth/logout')
      })
    }
  }
}
</script>

<style>
body {
  background: #f5f6fa;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  min-height: 100vh;
}
.app-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background: #fff;
  padding: 18px 32px 18px 32px;
  border-bottom: 1px solid #ececec;
}
.logo {
  font-size: 26px;
  font-weight: 900;
  color: #00a86b;
  letter-spacing: 1px;
  margin-right: 32px;
}
.quotes-bar-header {
  display: flex;
  gap: 16px;
  margin-right: 32px;
  font-size: 15px;
  font-weight: 600;
  color: #00a86b;
  min-width: 220px;
}
.quote {
  color: #00a86b;
  font-weight: 600;
  font-size: 15px;
}
.search-bar {
  flex: 1;
  margin: 0 32px;
  padding: 10px 18px;
  border-radius: 12px;
  border: 1px solid #ececec;
  background: #f6f6f6;
  font-size: 16px;
  max-width: 400px;
}
.catalog-icon-header {
  display: flex;
  align-items: center;
  margin-right: 32px;
  cursor: pointer;
  transition: background 0.2s;
  border-radius: 8px;
  padding: 4px;
}
.catalog-icon-header:hover {
  background: #e6f7ef;
}
.user-info {
  display: flex;
  align-items: center;
  font-size: 17px;
  color: #888;
  font-weight: 600;
}
.logout-btn {
  background: none;
  border: none;
  margin-left: 12px;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: background 0.2s;
  display: flex;
  align-items: center;
}
.logout-btn:hover {
  background: #f6f6f6;
}
.logout-btn svg {
  display: block;
}
.app-layout {
  display: flex;
  min-height: calc(100vh - 60px);
}
.side-nav {
  width: 210px;
  background: #f7f8fa;
  padding: 32px 0 0 0;
  border-right: 1px solid #ececec;
  min-height: 100vh;
}
.side-nav nav {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.side-nav a {
  display: flex;
  align-items: center;
  font-size: 18px;
  color: #222;
  text-decoration: none;
  padding: 10px 28px;
  border-radius: 8px 0 0 8px;
  transition: background 0.2s, color 0.2s;
}
.side-nav a.active, .side-nav a:hover {
  background: #e6f7ef;
  color: #00a86b;
}
.icon-nav {
  margin-right: 12px;
  font-size: 20px;
}
.main-content {
  flex: 1;
  padding: 36px 36px 36px 36px;
  background: #f5f6fa;
  min-height: 100vh;
}
.sidebar li.active a {
  font-weight: bold;
  color: #00a86b;
}
</style>