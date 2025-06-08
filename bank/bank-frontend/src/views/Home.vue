<template>
  <div class="home-page">
    <section class="wallet-block">
      <div class="wallet-header">
        <h2>Кошелёк</h2>
      </div>
      <div class="wallet-accounts">
        <div v-for="account in topAccounts" :key="account.account_number" class="wallet-account-card" @click="$router.push(`/accounts/${account.account_id}`)" style="cursor:pointer;">
          <div class="wallet-account-title">{{ account.account_name || ('№ ' + account.account_number) }}</div>
          <div class="wallet-account-balance">{{ account.balance }} {{ account.currency }}</div>
        </div>
      </div>
    </section>
    <!-- Здесь могут быть другие блоки: история, переводы и т.д. -->
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL, API_ENDPOINTS } from '@/config'

export default {
  name: 'HomeView',
  data() {
    return {
      accounts: []
    }
  },
  computed: {
    topAccounts() {
      // Сортируем по балансу и берём топ-3
      return [...this.accounts].sort((a, b) => Number(b.balance) - Number(a.balance)).slice(0, 3)
    }
  },
  async mounted() {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.ACCOUNTS.LIST}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      this.accounts = response.data
    } catch (e) {
      this.accounts = []
    }
  }
}
</script>

<style scoped>
.home-page {
  max-width: 900px;
  margin: 0 auto;
}
.wallet-block {
  background: linear-gradient(90deg, #e6eafc 0%, #f6f6fa 100%);
  border-radius: 24px;
  padding: 32px 32px 24px 32px;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.wallet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.wallet-header h2 {
  font-size: 24px;
  font-weight: 800;
  margin: 0;
}
.wallet-accounts {
  display: flex;
  gap: 24px;
}
.wallet-account-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 24px 32px 18px 32px;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: box-shadow 0.2s;
}
.wallet-account-card:hover {
  box-shadow: 0 4px 16px rgba(0,168,107,0.12);
}
.wallet-account-title {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #00a86b;
}
.wallet-account-balance {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 8px;
}
</style>