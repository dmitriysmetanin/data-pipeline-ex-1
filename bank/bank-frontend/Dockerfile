FROM node:16

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install

# Копирование проекта
COPY . .

# Создание пользователя без прав root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Порт для Vue.js
EXPOSE 8080

# Запуск приложения
CMD ["npm", "run", "serve"] 