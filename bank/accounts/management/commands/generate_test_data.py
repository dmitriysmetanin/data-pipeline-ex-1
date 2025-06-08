from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Customer
from django.db import transaction
import random
from faker import Faker

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Генерирует тестовые данные пользователей и клиентов'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем генерацию тестовых данных...')
        
        # Количество записей для генерации
        num_records = 50000
        
        # Размер батча для оптимизации производительности
        batch_size = 50000
        
        for i in range(0, num_records, batch_size):
            current_batch_size = min(batch_size, num_records - i)
            users_to_create = []
            customers_to_create = []
            
            with transaction.atomic():
                # Генерируем пользователей
                for _ in range(current_batch_size):
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    email = fake.email()
                    username = f"{first_name.lower()}{last_name.lower()}{random.randint(1000, 9999)}"
                    
                    user = User(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        is_active=True
                    )
                    user.set_password('testpass123')  # Устанавливаем одинаковый пароль для всех тестовых пользователей
                    users_to_create.append(user)
                
                # Создаем пользователей
                created_users = User.objects.bulk_create(users_to_create)
                
                # Генерируем клиентов
                for user in created_users:
                    customer = Customer(
                        user=user,
                        email=user.email,  # Используем email из пользователя
                        phone_number=fake.phone_number(),
                        address=fake.address(),
                        birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80)
                    )
                    customers_to_create.append(customer)
                
                # Создаем клиентов
                Customer.objects.bulk_create(customers_to_create)
            
            self.stdout.write(f'Создано {i + current_batch_size} записей из {num_records}')
        
        self.stdout.write(self.style.SUCCESS('Генерация тестовых данных завершена!')) 