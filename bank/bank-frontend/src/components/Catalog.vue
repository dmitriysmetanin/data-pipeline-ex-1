<template>
  <div class="catalog-page">
    <h2>Все сервисы</h2>
    <div class="catalog-tabs">
      <button :class="{active: activeTab === 'fin'}" @click="activeTab = 'fin'">Финансы</button>
      <button :class="{active: activeTab === 'eco'}" @click="activeTab = 'eco'">Экосистема</button>
      <button :class="{active: activeTab === 'gos'}" @click="activeTab = 'gos'">Госуслуги</button>
    </div>
    <div v-if="activeTab === 'fin'">
      <section class="catalog-block">
        <h3>Кошелёк</h3>
        <ul>
          <li><span class="icon card"></span> Оформить дебетовую карту</li>
          <li><span class="icon credit-card"></span> Оформить кредитную карту</li>
          <li><span class="icon money"></span> <router-link to="/accounts" class="catalog-link">Платёжные счета</router-link></li>
        </ul>
      </section>
      <section class="catalog-block">
        <h3>Вклады и цели</h3>
        <ul>
          <li><span class="icon deposit"></span> Вклады и счета</li>
          <li><span class="icon metal"></span> Металлические счета</li>
        </ul>
      </section>
      <section class="catalog-block">
        <h3>Кредиты</h3>
        <ul>
          <li><span class="icon consumer"></span> Потребительский кредит</li>
          <li><span class="icon potential"></span> Кредитный потенциал</li>
          <li><span class="icon history"></span> Кредитная история</li>
          <li><span class="icon all"></span> Все кредиты</li>
        </ul>
      </section>
      <section class="catalog-block">
        <h3>Инвестиции и пенсии</h3>
        <ul>
          <li><span class="icon invest"></span> Инвестиции</li>
          <li><span class="icon pension"></span> Пенсионные программы</li>
        </ul>
      </section>
    </div>
    <div v-else class="catalog-empty">
      <p>В этом разделе пока нет сервисов.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CatalogView',
  data() {
    return {
      activeTab: 'fin'
    }
  }
}
</script>

<style scoped>
.catalog-page {
  max-width: 700px;
  margin: 0 auto;
  background: #f6f6f6;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.catalog-tabs {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}
.catalog-tabs button {
  background: #ededed;
  border: none;
  border-radius: 8px 8px 0 0;
  padding: 8px 24px;
  font-size: 16px;
  cursor: pointer;
  color: #888;
  font-weight: 600;
}
.catalog-tabs button.active {
  background: #fff;
  color: #222;
}
.catalog-block {
  background: #fff;
  border-radius: 12px;
  margin-bottom: 24px;
  padding: 20px 24px 8px 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
.catalog-block h3 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 20px;
  font-weight: 700;
}
.catalog-block ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.catalog-block li {
  display: flex;
  align-items: center;
  padding: 8px 0;
  font-size: 16px;
  border-bottom: 1px solid #f0f0f0;
}
.catalog-block li:last-child {
  border-bottom: none;
}
.icon {
  display: inline-block;
  width: 22px;
  height: 22px;
  margin-right: 12px;
  background-size: contain;
  background-repeat: no-repeat;
}
.icon.card { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="%2300a86b"/><rect x="2" y="10" width="20" height="2" fill="%23fff"/></svg>'); }
.icon.credit-card { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="%2300a86b"/><rect x="2" y="10" width="20" height="2" fill="%23fff"/><rect x="16" y="16" width="4" height="2" fill="%23fff"/></svg>'); }
.icon.money { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="%2300a86b"/><circle cx="12" cy="12" r="3" fill="%23fff"/></svg>'); }
.icon.deposit { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="8" width="16" height="8" rx="2" fill="%2300a86b"/><rect x="8" y="4" width="8" height="4" rx="1" fill="%2300a86b"/></svg>'); }
.icon.metal { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="%2300a86b"/><rect x="8" y="8" width="8" height="8" fill="%23fff"/></svg>'); }
.icon.consumer { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="%2300a86b"/><rect x="6" y="10" width="12" height="2" fill="%23fff"/></svg>'); }
.icon.potential { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="8" width="16" height="8" rx="2" fill="%2300a86b"/><circle cx="12" cy="12" r="2" fill="%23fff"/></svg>'); }
.icon.history { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="%2300a86b"/><rect x="10" y="10" width="4" height="4" fill="%23fff"/></svg>'); }
.icon.all { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="%2300a86b"/><rect x="6" y="10" width="12" height="2" fill="%23fff"/><rect x="6" y="14" width="12" height="2" fill="%23fff"/></svg>'); }
.icon.invest { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="%2300a86b"/><rect x="10" y="10" width="4" height="4" fill="%23fff"/></svg>'); }
.icon.pension { background-image: url('data:image/svg+xml;utf8,<svg fill="%2300a86b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="8" width="16" height="8" rx="2" fill="%2300a86b"/><rect x="8" y="12" width="8" height="2" fill="%23fff"/></svg>'); }
.catalog-empty {
  text-align: center;
  color: #aaa;
  margin-top: 40px;
  font-size: 18px;
}
.catalog-link {
  color: #222;
  text-decoration: underline;
  font-weight: 500;
  transition: color 0.2s;
}
.catalog-link:hover {
  color: #00a86b;
}
</style> 