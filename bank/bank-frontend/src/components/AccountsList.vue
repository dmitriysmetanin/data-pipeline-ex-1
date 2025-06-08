<template>
  <div class="accounts-list-page">
    <h2>Платёжные счета</h2>
    <button class="open-account-btn" @click="$router.push('/accounts/open')">Открыть платёжный счёт</button>
    <div v-if="accounts.length === 0" class="no-accounts-block">
      <div class="sad-turtle">
        <svg width="120" height="80" viewBox="0 0 120 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="60" cy="60" rx="40" ry="18" fill="#b0c4b1"/>
          <ellipse cx="60" cy="48" rx="32" ry="22" fill="#6b8e23"/>
          <ellipse cx="60" cy="48" rx="26" ry="16" fill="#8fbc8f"/>
          <ellipse cx="40" cy="62" rx="6" ry="4" fill="#b0c4b1"/>
          <ellipse cx="80" cy="62" rx="6" ry="4" fill="#b0c4b1"/>
          <ellipse cx="60" cy="38" rx="8" ry="6" fill="#b0c4b1"/>
          <ellipse cx="56" cy="37" rx="1.5" ry="2" fill="#222"/>
          <ellipse cx="64" cy="37" rx="1.5" ry="2" fill="#222"/>
          <path d="M57 41 Q60 44 63 41" stroke="#222" stroke-width="1.5" fill="none"/>
        </svg>
      </div>
      <div class="no-accounts-text">Ой... Не создано ни одного счета!</div>
    </div>
    <div v-else class="accounts-grid">
      <div v-for="account in accounts" :key="account.account_number" class="account-card" @click="$router.push(`/accounts/${account.account_id}`)" style="cursor:pointer;">
        <div class="account-title">{{ account.account_name || ('№ ' + account.account_number) }}</div>
        <div class="account-balance">{{ account.balance }} {{ account.currency }}</div>
        <div class="account-status">Статус: {{ account.status }}</div>
        <div class="account-dates">
          Открыт: {{ new Date(account.open_date).toLocaleDateString() }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AccountsList',
  data() {
    return {
      accounts: []
    }
  },
  async mounted() {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:8000/api/accounts/my/', {
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
.accounts-list-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 16px;
}
.accounts-list-page h2 {
  margin-bottom: 32px;
  text-align: left;
}
.open-account-btn {
  background: #00a86b;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 28px;
  cursor: pointer;
  transition: background 0.2s;
}
.open-account-btn:hover {
  background: #00915c;
}
.no-accounts-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 48px;
}
.sad-turtle {
  margin-bottom: 18px;
}
.no-accounts-text {
  font-size: 20px;
  color: #888;
  font-weight: 500;
}
.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}
.account-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 24px 20px 18px 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: box-shadow 0.2s;
}
.account-card:hover {
  box-shadow: 0 4px 16px rgba(0,168,107,0.12);
}
.account-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #00a86b;
}
.account-balance {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 8px;
}
.account-status {
  font-size: 15px;
  color: #888;
  margin-bottom: 8px;
}
.account-dates {
  font-size: 14px;
  color: #aaa;
}
</style> 