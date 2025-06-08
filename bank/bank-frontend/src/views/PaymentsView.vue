<template>
  <div class="payments-page">
    <h2>Платежи</h2>

    <section class="payments-section frequent-payments">
      <h3>Часто используемые</h3>
      <div class="frequent-grid">
        <div class="frequent-item">
          <div class="frequent-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><rect x="7" y="7" width="10" height="10" rx="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          Оплатить по QR-коду
        </div>
        <div class="frequent-item">
           <div class="frequent-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="9 22 9 12 15 12 15 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          Дом
        </div>
        <div class="frequent-item">
           <div class="frequent-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16v6M15 10l-3 3-3-3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          КФУ Приволжский
        </div>
        <div class="frequent-item">
           <div class="frequent-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 6l-10 7L2 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          Летай
        </div>
        <div class="frequent-item">
           <div class="frequent-icon"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 16.92V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-3.08A6 6 0 0 1 8.15 12a6 6 0 0 1 7.7 0A6 6 0 0 1 22 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 12V2M5 5l4 4M19 5l-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          МегаФон
        </div>
      </div>
    </section>

    <section class="payments-section transfer-section">
      <h3>Перевести</h3>
      <router-link to="/payments/transfer" class="transfer-option">
        На Сбер или в другой банк
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </router-link>
       <!-- Placeholder for frequent transfers -->
       <div class="frequent-transfers">
         <!-- Example placeholders - replace with data later -->
         <div class="transfer-user">
           <div class="user-avatar">ДЮ</div>
           Дмитрий Юрьевич
         </div>
          <div class="transfer-user">
           <div class="user-avatar">АВ</div>
           Андрей Владимирович...
         </div>
       </div>
    </section>

    <section class="payments-section payment-categories">
      <h3>Оплатить</h3>
      <ul>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="18" height="18" rx="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Оплата по QR</li>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Дом</li>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22 16.92V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-3.08A6 6 0 0 1 8.15 12a6 6 0 0 1 7.7 0A6 6 0 0 1 22 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Мобильная связь</li>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="5" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 19L8 15M16 19L16 15M2 12h20M6 15l2-3 2 3M14 15l2-3 2 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Транспорт</li>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Государство</li>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 17l-2 4m2-4l2 4m-2-4v-7.5a4.5 4.5 0 1 1 9 0V17m0 0v-7.5a4.5 4.5 0 1 0-9 0V17m0 0h18M10 22h4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Образование</li>
        <li><span class="icon-category"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Отдых и развлечения</li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  name: 'PaymentsView',
}
</script>

<style scoped>
.payments-page {
  max-width: 900px;
  margin: 0 auto;
}

.payments-page h2 {
  margin-bottom: 24px;
  font-size: 28px;
  font-weight: 800;
}

.payments-section {
  background: #fff;
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.payments-section h3 {
    font-size: 20px;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 16px;
}

.frequent-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px;
}

.frequent-item {
    background: #f7f8fa;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: background 0.2s;
}
.frequent-item:hover {
    background: #e6e9ed;
}

.frequent-icon {
    margin-bottom: 8px;
    color: #00a86b;
}

.transfer-option {
    background: #f7f8fa;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 16px;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
    transition: background 0.2s;
}
.transfer-option:hover {
     background: #e6e9ed;
}

.frequent-transfers {
    display: flex;
    gap: 16px;
    margin-top: 16px;
    overflow-x: auto;
    padding-bottom: 8px; /* To prevent scrollbar overlap */
}

.transfer-user {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 13px;
    min-width: 60px;
    text-align: center;
}

.user-avatar {
    width: 40px;
    height: 40px;
    background: #00a86b;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    margin-bottom: 4px;
}

.payment-categories ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.payment-categories li {
    padding: 12px 0;
    font-size: 16px;
    border-bottom: 1px solid #ececec;
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: background 0.1s;
}

.payment-categories li:hover {
    background: #f7f8fa;
}

.payment-categories li:last-child {
    border-bottom: none;
}

.icon-category {
    margin-right: 12px;
    color: #00a86b;
}
</style> 