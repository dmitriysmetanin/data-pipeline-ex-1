import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Создаем приложение
const app = createApp(App)

// Подключаем плагины
app.use(router)
app.use(store)

// Монтируем приложение
app.mount('#app')