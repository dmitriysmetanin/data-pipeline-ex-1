<template>
  <div class="transfer-page">
    <h2>Между своими счетами и картами</h2>

    <div class="transfer-details">
      <h3>Детали перевода</h3>
      
      <div class="form-group">
        <label for="fromAccount">Откуда</label>
        <select id="fromAccount" v-model="selectedFromAccount" @change="filterToAccounts">
          <option value="" disabled>Выберите счет</option>
          <option v-for="account in accounts" :key="account.account_id" :value="account">
            {{ account.account_name || ('Счет № ' + account.account_number) }} ({{ account.balance }} {{ account.currency }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="toAccount">Куда</label>
        <select id="toAccount" v-model="selectedToAccount" :disabled="!selectedFromAccount">
          <option value="" disabled>Выберите счет</option>
          <option v-for="account in filteredToAccounts" :key="account.account_id" :value="account">
             {{ account.account_name || ('Счет № ' + account.account_number) }} ({{ account.balance }} {{ account.currency }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="amount">Сколько</label>
        <input type="number" id="amount" v-model="amount" placeholder="Введите сумму">
        <button v-if="selectedFromAccount" @click="useMaxAmount">Все {{ selectedFromAccount.balance }} {{ selectedFromAccount.currency }}</button>
      </div>

      <button class="continue-button" @click="showConfirmation" :disabled="!selectedFromAccount || !selectedToAccount || !amount || amount <= 0">Продолжить</button>
    </div>

    <div class="confirmation-section" v-if="showConfirmationSection">
      <h3>Подтверждение</h3>
      <p>Перевод с {{ selectedFromAccount?.account_name || ('Счет № ' + selectedFromAccount?.account_number) }} на {{ selectedToAccount?.account_name || ('Счет № ' + selectedToAccount?.account_number) }}</p>
      <p>Сумма: {{ amount }} {{ selectedFromAccount?.currency }}</p>
      <button class="confirm-button" @click="confirmTransfer">Перевести {{ amount }} {{ selectedFromAccount?.currency }}</button>
      <button class="cancel-button" @click="cancelConfirmation">Отменить</button>
    </div>

  </div>
</template>

<script>

export default {
  data() {
    return {
      accounts: [],
      selectedFromAccount: null,
      selectedToAccount: null,
      amount: null,
      showConfirmationSection: false,
    };
  },
  computed: {
    filteredToAccounts() {
      if (!this.selectedFromAccount) {
        return [];
      }
      // Фильтруем счета, оставляя только те, что в той же валюте и не являются выбранным счетом "Откуда"
      return this.accounts.filter(account => 
        account.currency === this.selectedFromAccount.currency && 
        account.account_id !== this.selectedFromAccount.account_id
      );
    }
  },
  created() {
    this.fetchAccounts();
  },
  methods: {
    fetchAccounts() {
      // TODO: Реализовать получение списка счетов пользователя
      // Пример заглушки:
      this.accounts = [
        { account_id: 1, account_number: '3922', account_name: 'Платежный счет', balance: 217057.08, currency: '₽', open_date: '2023-01-15' },
        { account_id: 2, account_number: '3990', account_name: 'Платежный счет', balance: 295193.37, currency: '₽', open_date: '2023-02-20' },
        { account_id: 3, account_number: '1234', account_name: 'Сберегательный счет', balance: 1000.00, currency: '$', open_date: '2023-03-10' },
      ];
    },
    filterToAccounts() {
      // Эта функция вызывается автоматически при изменении selectedFromAccount благодаря computed property
      this.selectedToAccount = null; // Сбрасываем выбранный счет "Куда"
    },
    useMaxAmount() {
      if (this.selectedFromAccount) {
        this.amount = this.selectedFromAccount.balance;
      }
    },
    showConfirmation() {
      this.showConfirmationSection = true;
    },
    cancelConfirmation() {
      this.showConfirmationSection = false;
    },
    confirmTransfer() {
      // TODO: Реализовать логику перевода и переход на страницу-заглушку после успешного перевода
      alert('Перевод подтвержден!'); // Заглушка
      this.$router.push('/transfer-success-placeholder'); // Переход на страницу-заглушку успеха перевода
    },
  },
};
</script>

<style scoped>
.transfer-page {
  padding: 20px;
}

.transfer-details, .confirmation-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group select, .form-group input[type="number"] {
  width: calc(100% - 22px); /* Adjust for padding and border */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group button {
  margin-top: 5px;
  padding: 8px 12px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.continue-button, .confirm-button, .cancel-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 10px;
}

.continue-button, .confirm-button {
  background-color: #28a745;
  color: white;
}

.cancel-button {
  background-color: #ccc;
  color: #333;
  margin-left: 10px;
}
</style> 