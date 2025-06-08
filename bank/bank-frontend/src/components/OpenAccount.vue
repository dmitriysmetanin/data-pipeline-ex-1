<template>
  <div class="open-account-page">
    <!-- Шаг 1: Промо-блок -->
    <div v-if="step === 1" class="step step-promo">
      <div class="promo-content">
        <div class="promo-img">
          <!-- Можно заменить на реальное изображение -->
          <img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" alt="Медитирующий человек" style="width: 120px; height: 120px;" />
        </div>
        <div class="promo-info">
          <h2>Платёжный счёт.<br>Ещё одна карта не нужна</h2>
          <div class="promo-desc">Платите, переводите и планируйте повседневные расходы</div>
          <button class="main-btn" @click="step = 2">Открыть счёт</button>
        </div>
      </div>
      <div class="promo-features">
        <div class="feature">
          <span class="icon-box"><svg width="28" height="28" fill="none"><rect width="24" height="24" x="2" y="2" rx="6" fill="#F3F4F6"/><rect width="16" height="16" x="6" y="6" rx="4" fill="#222"/></svg></span>
          <div>
            <div class="feature-title">Планирование расходов</div>
            <div class="feature-desc">Сколько угодно бесплатных счетов для распределения расходов</div>
          </div>
        </div>
        <div class="feature">
          <span class="icon-box"><svg width="28" height="28" fill="none"><rect width="24" height="24" x="2" y="2" rx="6" fill="#F3F4F6"/><circle cx="14" cy="14" r="7" fill="#222"/></svg></span>
          <div>
            <div class="feature-title">Покупки со SberPay</div>
            <div class="feature-desc">Начислим бонусы Спасибо, как по карте</div>
          </div>
        </div>
        <div class="feature">
          <span class="icon-box"><svg width="28" height="28" fill="none"><rect width="24" height="24" x="2" y="2" rx="6" fill="#F3F4F6"/><rect width="16" height="8" x="6" y="10" rx="4" fill="#222"/></svg></span>
          <div>
            <div class="feature-title">Снятие наличных в банкоматах</div>
            <div class="feature-desc">Без карты по QR-коду</div>
          </div>
        </div>
      </div>
      <div class="promo-card-block">
        <div class="promo-card-title">А если понадобится карта или стикер?</div>
        <div class="promo-card-desc">Оформите их или добавьте к счёту уже действующую</div>
        <img src="https://cdn-icons-png.flaticon.com/512/1048/1048956.png" alt="Карта" style="width: 120px; height: 60px; margin-top: 10px;" />
      </div>
      <div class="promo-docs">
        <div class="docs-title">Документы</div>
        <ul class="docs-list">
          <li><span class="icon-doc"></span> Условия по платёжному счёту</li>
          <li><span class="icon-doc"></span> Подробнее о тарифе</li>
        </ul>
      </div>
    </div>

    <!-- Шаг 2: Параметры счёта -->
    <div v-else-if="step === 2" class="step step-params">
      <h2>Открытие платёжного счёта</h2>
      <div class="params-block">
        <div class="params-title">Параметры счёта</div>
        <div class="params-field">
          <label>Название счёта</label>
          <input type="text" v-model="accountName" placeholder="Введите название счёта" />
          <div class="field-desc">Название можно будет поменять в любой момент</div>
        </div>
        <div class="params-field">
          <label>Валюта счёта</label>
          <select v-model="currency">
            <option value="RUB">Рубли</option>
            <option value="USD">Доллары</option>
            <option value="EUR">Евро</option>
            <option value="CNY">Юани</option>
          </select>
        </div>
      </div>
      <button class="main-btn" @click="step = 3">Продолжить</button>
    </div>

    <!-- Шаг 3: Документы -->
    <div v-else-if="step === 3" class="step step-docs">
      <div class="params-block params-block-collapsed">
        <div class="params-title">Параметры счёта <span class="params-check">&#10003;</span></div>
      </div>
      <div class="docs-block">
        <div class="docs-title">Список документов</div>
        <div class="docs-desc">Ознакомьтесь с документами и подтвердите свое согласие</div>
        <ul class="docs-list">
          <li><span class="icon-doc"></span> Заявление на открытие платёжного счёта</li>
          <li><span class="icon-doc"></span> Памятка по платёжному счёту</li>
          <li><span class="icon-doc"></span> Условия открытия и обслуживания платёжного счёта</li>
          <li><span class="icon-doc"></span> Условия тарифа по платёжному счёту</li>
        </ul>
        <div class="docs-agree">
          <input type="checkbox" id="agree" v-model="agree" />
          <label for="agree">Я соглашаюсь с условиями и подписываю документы на открытие платёжного счёта</label>
        </div>
        <button class="main-btn" :disabled="!agree || loading" @click="createAccount">Подтвердить</button>
        <button class="cancel-btn" @click="step = 2">Отменить</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL, API_ENDPOINTS } from '@/config'

export default {
  name: 'OpenAccount',
  data() {
    return {
      step: 1,
      accountName: 'Платёжный счёт',
      currency: 'RUB',
      agree: false,
      loading: false
    }
  },
  methods: {
    async createAccount() {
      if (!this.agree || this.loading) return
      this.loading = true
      try {
        const token = localStorage.getItem('token')
        await axios.post(`${API_BASE_URL}${API_ENDPOINTS.ACCOUNTS.CREATE}`, {
          status: 'active',
          balance: 0,
          currency: this.currency,
          account_name: this.accountName
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.$router.push('/accounts')
      } catch (e) {
        alert('Ошибка при создании счёта')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.open-account-page {
  max-width: 600px;
  margin: 40px auto;
  background: #f6f6f6;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 32px 24px 40px 24px;
}
.step-promo {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.promo-content {
  display: flex;
  gap: 32px;
  align-items: center;
}
.promo-img {
  flex-shrink: 0;
}
.promo-info h2 {
  margin: 0 0 8px 0;
  font-size: 22px;
  font-weight: 700;
}
.promo-desc {
  color: #888;
  margin-bottom: 18px;
}
.main-btn {
  background: #00a86b;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 32px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s;
}
.main-btn:disabled {
  background: #b0c4b1;
  cursor: not-allowed;
}
.main-btn:hover:not(:disabled) {
  background: #00915c;
}
.promo-features {
  display: flex;
  gap: 18px;
  margin-bottom: 12px;
}
.feature {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  background: #fff;
  border-radius: 12px;
  padding: 14px 16px;
  flex: 1;
  min-width: 0;
}
.icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: #f3f4f6;
  border-radius: 8px;
}
.feature-title {
  font-weight: 600;
  font-size: 15px;
}
.feature-desc {
  color: #888;
  font-size: 13px;
}
.promo-card-block {
  background: #fff;
  border-radius: 12px;
  padding: 18px 20px 10px 20px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 18px;
}
.promo-card-title {
  font-weight: 600;
  font-size: 16px;
}
.promo-card-desc {
  color: #888;
  font-size: 13px;
}
.promo-docs {
  background: #fff;
  border-radius: 12px;
  padding: 18px 20px 10px 20px;
  margin-bottom: 0;
}
.docs-title {
  font-weight: 700;
  font-size: 17px;
  margin-bottom: 8px;
}
.docs-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.docs-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  margin-bottom: 6px;
}
.icon-doc {
  display: inline-block;
  width: 22px;
  height: 22px;
  background: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4" fill="%2300a86b"/><text x="12" y="17" font-size="10" text-anchor="middle" fill="white">pdf</text></svg>') center/contain no-repeat;
}
.step-params {
  background: #fff;
  border-radius: 16px;
  padding: 32px 24px 24px 24px;
}
.params-block {
  background: #f6f6f6;
  border-radius: 12px;
  padding: 20px 18px 10px 18px;
  margin-bottom: 24px;
}
.params-title {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 16px;
}
.params-field {
  margin-bottom: 18px;
}
.params-field label {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 4px;
  display: block;
}
.params-field input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: #f3f4f6;
  font-size: 16px;
  margin-bottom: 4px;
}
.field-desc {
  color: #888;
  font-size: 12px;
}
.params-field select {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background: #f3f4f6;
  font-size: 16px;
  margin-bottom: 4px;
}
.step-docs {
  background: #fff;
  border-radius: 16px;
  padding: 32px 24px 24px 24px;
}
.params-block-collapsed {
  padding: 12px 18px;
  margin-bottom: 18px;
  background: #f6f6f6;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.params-check {
  color: #00a86b;
  font-size: 22px;
  font-weight: 700;
  margin-left: 8px;
}
.docs-block {
  background: #f6f6f6;
  border-radius: 12px;
  padding: 20px 18px 10px 18px;
}
.docs-desc {
  color: #888;
  font-size: 13px;
  margin-bottom: 12px;
}
.docs-agree {
  margin: 18px 0 18px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
.cancel-btn {
  background: none;
  color: #00a86b;
  border: none;
  font-size: 16px;
  font-weight: 500;
  margin-top: 10px;
  cursor: pointer;
  text-decoration: underline;
}
.cancel-btn:hover {
  color: #00915c;
}
</style> 