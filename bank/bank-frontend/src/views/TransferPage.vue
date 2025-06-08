<template>
  <div class="transfer-page">
    <div class="transfer-header">
      <router-link to="/payments" class="back-link">← Назад</router-link>
      <h2>Новый перевод</h2>
    </div>

    <div class="transfer-steps">
      <!-- Step 1: Enter Recipient Info -->
      <section v-if="currentStep === 'initial' || currentStep === 'recipientFound'" class="transfer-section">
        <h3>Получатель</h3>
        <div class="recipient-input-container">
          <input
            type="text"
            placeholder="Номер счета (16 цифр)"
            v-model="recipientInput"
            @input="checkRecipient"
            maxlength="16"
            class="input-field"
          />
           <svg v-if="currentStep === 'recipientFound'" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M8 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <div v-if="currentStep === 'recipientFound'" class="recipient-details">
          <p>ФИО получателя:</p>
          <p class="recipient-name">{{ recipientName }}</p>
           <div class="info-box">
             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
             Пожалуйста, проверьте имя. Если всё хорошо, нажмите «Продолжить»
           </div>
        </div>
        <button v-if="currentStep === 'recipientFound'" class="continue-button" @click="nextStep">Продолжить</button>
        <div v-else-if="recipientError">
          <p style="color: red">{{ recipientError }}</p>
        </div>
      </section>

      <!-- Step 2: Enter Transfer Details -->
      <section v-if="currentStep === 'details'" class="transfer-section">
        <h3>Детали перевода</h3>
         <div class="detail-item">
           <label>Счёт списания</label>
           <select v-model="selectedAccount" class="input-field">
             <option value="" disabled>Выберите счет</option>
             <option v-for="account in userAccounts" :key="account.account_id" :value="account.account_id">
               {{ account.account_name || 'Счет' }} {{ account.account_number.slice(-4) }} (Баланс: {{ account.balance }} {{ account.currency }})
             </option>
           </select>
         </div>
         <div class="detail-item">
           <label>Сумма</label>
           <input type="number" placeholder="Сумма перевода" v-model="amount" class="input-field"/>
         </div>
         <div class="detail-item">
           <label>Сообщение получателю (необязательно)</label>
           <input type="text" placeholder="Сообщение" v-model="message" class="input-field" maxlength="40"/>
            <span class="char-count">{{ message.length }} / 40</span>
         </div>
         <button class="continue-button" @click="nextStep" :disabled="!selectedAccount || !amount">Продолжить</button>
      </section>

      <!-- Step 3: Confirmation (Placeholder for SMS code) -->
      <section v-if="currentStep === 'confirmation'" class="transfer-section">
        <h3>Подтверждение</h3>
         <!-- Placeholder for SMS code input -->
         <p>Введите код из СМС</p>
         <input type="text" placeholder="Код" class="input-field"/>
         <button class="continue-button" @click="nextStep">Подтвердить</button>
      </section>

       <!-- Step 4: Result -->
      <section v-if="currentStep === 'result'" class="transfer-section transfer-result">
        <div class="success-icon">
           <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" fill="#00a86b" stroke="#00a86b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 12l2 2 4-4" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <h3>Перевод доставлен</h3>
        <p class="transfer-amount">{{ amount }} ₽</p>
        <p class="transfer-recipient-name">{{ recipientName }}</p>
         <div class="result-details">
           <h4>Подробности операции</h4>
           <div class="detail-row"><span class="detail-label">Счёт списания</span> <span class="detail-value">Платежный счёт -- 3990</span></div>
            <div class="detail-row"><span class="detail-label">ФИО получателя</span> <span class="detail-value">{{ recipientName }}</span></div>
            <div class="detail-row"><span class="detail-label">Телефон получателя</span> <span class="detail-value">{{ recipientInput }}</span></div>
            <div class="detail-row"><span class="detail-label">Сумма перевода</span> <span class="detail-value">{{ amount }} ₽</span></div>
            <div class="detail-row"><span class="detail-label">Комиссия</span> <span class="detail-value">0 ₽</span></div>
            <div class="detail-row"><span class="detail-label">Сообщение получателю</span> <span class="detail-value">{{ message || '-' }}</span></div>
             <!-- Placeholder for other details -->
             <div class="detail-row"><span class="detail-label">Дополнительная информация</span> <span class="detail-value info-text">Если вы отправили деньги не тому человеку, обратитесь к получателю перевода.<br/> Деньги может внести только отправитель</span></div>
            <div class="detail-row"><span class="detail-label">Номер документа</span> <span class="detail-value">1000000007555332205</span></div>
            <div class="detail-row"><span class="detail-label">Дата документа</span> <span class="detail-value">05.06.2023</span></div>
         </div>
         <div class="result-actions">
           <button class="action-button"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="10 9 9 9 8 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Сохранить чек</button>
           <button class="action-button"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 15l-3-3 3-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 12h7M21 12a9 9 0 0 1-9 9c-2.52 0-4.93-.67-7-1.8M3 12a9 9 0 0 0 14.9-8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Создать шаблон</button>
         </div>
      </section>

      <!-- Placeholder sections for steps (for visual structure) -->
       <div class="step-placeholder" :class="{ active: currentStep === 'details' || currentStep === 'confirmation' || currentStep === 'result' }">Детали перевода</div>
      <div class="step-placeholder" :class="{ active: currentStep === 'confirmation' || currentStep === 'result' }">Подтверждение</div>
       <div v-if="currentStep !== 'result'" class="step-placeholder" :class="{ active: currentStep === 'result' }">Результат</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL, API_ENDPOINTS } from '@/config'

export default {
  name: 'TransferPage',
  data() {
    return {
      currentStep: 'initial',
      recipientInput: '',
      recipientName: '',
      recipientError: '',
      amount: null,
      message: '',
      userAccounts: [],
      selectedAccount: '',
    }
  },
  watch: {
      recipientInput(newValue) {
          this.checkRecipient(newValue);
      }
  },
  methods: {
    async checkRecipient(input) {
      this.recipientError = ''
      this.recipientName = ''
      if (/^\d{16}$/.test(input)) {
        try {
          const token = localStorage.getItem('token')
          if (!token) {
            this.recipientError = 'Необходима авторизация.'
            return
          }
          const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.ACCOUNTS.LOOKUP}?account_number=${input}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })
          if (response.data && response.data.name) {
            this.recipientName = response.data.name
            this.currentStep = 'recipientFound'
          } else {
            this.recipientError = 'такой платежный счет отсутствует'
            this.currentStep = 'initial'
          }
        } catch (error) {
          if (error.response && error.response.status === 404) {
            this.recipientError = 'такой платежный счет отсутствует'
          } else {
            this.recipientError = 'Ошибка при поиске счета'
          }
          this.currentStep = 'initial'
        }
      } else {
        this.recipientError = ''
        this.recipientName = ''
        this.currentStep = 'initial'
      }
    },
    nextStep() {
      if (this.currentStep === 'recipientFound') {
        this.currentStep = 'details'
      } else if (this.currentStep === 'details') {
        this.currentStep = 'confirmation'
      } else if (this.currentStep === 'confirmation') {
        this.currentStep = 'result'
      }
    },
    async fetchUserAccounts() {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          this.userAccounts = []
          return
        }
        const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.ACCOUNTS.LIST}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        this.userAccounts = response.data
      } catch (error) {
        this.userAccounts = []
      }
    }
  },
  mounted() {
    this.fetchUserAccounts()
  }
}
</script>

<style scoped>
.transfer-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 24px;
}

.transfer-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.back-link {
  display: inline-block;
  margin-right: 16px;
  color: #00a86b;
  text-decoration: none;
  font-weight: 500;
  font-size: 18px;
}

.back-link:hover {
  text-decoration: underline;
}

.transfer-header h2 {
  font-size: 28px;
  font-weight: 800;
  margin: 0;
}

.transfer-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.transfer-section {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.transfer-section h3 {
    font-size: 20px;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 16px;
}

.recipient-input-container {
  display: flex;
  align-items: center;
  border: 1px solid #ececec;
  border-radius: 12px;
  padding: 10px 16px;
  margin-bottom: 16px;
}

.recipient-input-container input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  padding: 0;
}

.recipient-input-container svg {
   color: #00a86b;
   margin-left: 8px;
}

.recipient-details {
   margin-bottom: 16px;
}
.recipient-details p {
   margin: 4px 0;
   font-size: 15px;
   color: #555;
}
.recipient-name {
   font-weight: 600;
   color: #222;
   font-size: 16px;
}

.info-box {
   display: flex;
   align-items: flex-start;
   background: #e6f7ef;
   border: 1px solid #ccecdb;
   border-radius: 12px;
   padding: 12px 16px;
   font-size: 14px;
   color: #333;
   margin-top: 16px;
}

.info-box svg {
   color: #00a86b;
   margin-right: 8px;
   min-width: 18px;
}

.continue-button {
  display: block;
  width: 100%;
  padding: 14px;
  background-color: #00a86b;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.continue-button:hover {
  background-color: #00955a;
}

.detail-item {
   margin-bottom: 16px;
}

.detail-item label {
   display: block;
   font-size: 14px;
   color: #555;
   margin-bottom: 4px;
}

.detail-item .input-field {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ececec;
  border-radius: 12px;
  font-size: 16px;
  outline: none;
}

.detail-item .char-count {
   display: block;
   text-align: right;
   font-size: 12px;
   color: #888;
   margin-top: 4px;
}

.account-select {
   width: 100%;
   padding: 10px 12px;
   border: 1px solid #ececec;
   border-radius: 12px;
   font-size: 16px;
   display: flex;
   justify-content: space-between;
   align-items: center;
   cursor: pointer;
   color: #222;
}

.step-placeholder {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  color: #bbb;
  font-size: 20px;
  font-weight: 700;
   opacity: 0.6;
}

.step-placeholder.active {
   opacity: 1;
}

.transfer-result {
   text-align: center;
}

.success-icon {
   margin-bottom: 16px;
   color: #00a86b;
}

.transfer-amount {
   font-size: 24px;
   font-weight: 800;
   margin-bottom: 8px;
   color: #00a86b;
}

.transfer-recipient-name {
   font-size: 18px;
   font-weight: 600;
   color: #222;
   margin-bottom: 24px;
}

.result-details {
   text-align: left;
   margin-top: 24px;
   border-top: 1px solid #ececec;
   padding-top: 24px;
}

.result-details h4 {
   font-size: 18px;
   font-weight: 700;
   margin-bottom: 16px;
}

.detail-row {
   display: flex;
   justify-content: space-between;
   margin-bottom: 12px;
   font-size: 15px;
}

.detail-label {
   color: #555;
}

.detail-value {
   font-weight: 600;
   color: #222;
}

.info-text {
   font-weight: 400;
   color: #555;
   max-width: 60%;
   text-align: right;
   line-height: 1.4;
}

.result-actions {
   display: flex;
   gap: 16px;
   margin-top: 24px;
   justify-content: center;
}

.action-button {
   background: #f7f8fa;
   border: 1px solid #ececec;
   border-radius: 12px;
   padding: 10px 16px;
   font-size: 15px;
   font-weight: 600;
   cursor: pointer;
   display: flex;
   align-items: center;
   gap: 8px;
   color: #222;
   transition: background 0.2s;
}

.action-button:hover {
   background: #e6e9ed;
}

/* Add style for select element */
.transfer-section select.input-field {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2220%22%20height%3D%2220%22%20viewBox%3D%220%200%2020%2020%22%3E%3Cpath%20fill%3D%22%23666%22%20d%3D%22M0%206l10%2010%2010-10%22%2F%3E%3C%2Fsvg%3E");
    background-repeat: no-repeat;
    background-position: right 12px top 50%;
    background-size: 12px auto;
}

</style> 