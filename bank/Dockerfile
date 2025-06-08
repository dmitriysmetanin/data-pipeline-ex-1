FROM python:3.9

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование проекта
COPY . .

# Создание пользователя без прав root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Порт для Django
EXPOSE 8000

# Команда запуска будет указана в docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 