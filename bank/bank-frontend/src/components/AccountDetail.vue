<template>
  <div class="account-detail-page" v-if="account">
    <h2 class="account-header">{{ account.account_name ? account.account_name : 'Счет № ' + account.account_number }}</h2>
    <div class="account-info">
      <div><b>Номер счета:</b> {{ account.account_number }}</div>
      <div><b>Баланс:</b> {{ account.balance }} {{ account.currency }}</div>
      <div><b>Статус:</b> {{ account.status }}</div>
      <div><b>Дата открытия:</b> {{ new Date(account.open_date).toLocaleDateString() }}</div>
    </div>

    <div class="button-section">
      <button class="action-button" @click="goToDeposit">
        <i class="fas fa-plus-circle"></i> Пополнить
      </button>
      <button class="action-button" @click="goToTransfer">
        <i class="fas fa-exchange-alt"></i> Перевести
      </button>
      <button class="action-button" @click="goToSettings">
        <i class="fas fa-cog"></i> Настроить
      </button>
    </div>

    <div class="transactions-block">
      <h3>История транзакций</h3>
      <div v-if="transactions.length === 0" class="no-transactions">Нет транзакций</div>
      <table v-else class="transactions-table">
        <thead>
          <tr>
            <th>Дата</th>
            <th>Тип</th>
            <th>Сумма</th>
            <th>Описание</th>
            <th v-if="hasTransfers">Счет назначения</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in transactions" :key="tx.id">
            <td>{{ new Date(tx.transaction_date).toLocaleString() }}</td>
            <td>{{ txTypeLabel(tx.transaction_type) }}</td>
            <td>{{ tx.amount }}</td>
            <td>{{ tx.description }}</td>
            <td v-if="hasTransfers">{{ tx.transaction_type === 'transfer' ? tx.another_account : '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AccountDetail',
  data() {
    return {
      account: null,
      transactions: []
    }
  },
  computed: {
    hasTransfers() {
      return this.transactions.some(tx => tx.transaction_type === 'transfer')
    }
  },
  methods: {
    txTypeLabel(type) {
      if (type === 'deposit') return 'Пополнение'
      if (type === 'withdrawal') return 'Снятие'
      if (type === 'transfer') return 'Перевод'
      return type
    },
    goToDeposit() {
      this.$router.push('/deposit-placeholder');
    },
    goToTransfer() {
      this.$router.push('/transfer-between-own');
    },
    goToSettings() {
      this.$router.push('/settings-placeholder');
    },
  },
  async mounted() {
    const token = localStorage.getItem('token')
    const id = this.$route.params.id
    try {
      const accRes = await axios.get(`http://localhost:8000/api/accounts/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.account = accRes.data
      const txRes = await axios.get(`http://localhost:8000/api/transactions/?account_id=${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.transactions = txRes.data
    } catch (e) {
      this.account = null
      this.transactions = []
    }
  }
}
</script>

<style scoped>
.account-detail-page {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 32px 24px 40px 24px;
}
.account-info {
  margin-bottom: 28px;
  font-size: 17px;
  color: #222;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.transactions-block {
  margin-top: 32px;
}
.transactions-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}
.transactions-table th, .transactions-table td {
  border-bottom: 1px solid #ececec;
  padding: 8px 6px;
  text-align: left;
}
.transactions-table th {
  background: #f6f6f6;
  font-weight: 700;
}
.no-transactions {
  color: #aaa;
  font-size: 16px;
  margin-top: 18px;
}
.account-header {
  margin-bottom: 20px;
}
.button-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}
.action-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
}
.action-button i {
  margin-right: 8px;
}
</style> 