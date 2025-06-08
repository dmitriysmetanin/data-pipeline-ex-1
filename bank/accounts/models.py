from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    tax_id = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='user_id')
    created_dts = models.DateTimeField(auto_now=True)
    updated_dts = models.DateTimeField(auto_now=True)
    tg_id = models.BigIntegerField(null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = "customers"
        managed = True

class Account(models.Model):
    account_id = models.BigAutoField(primary_key=True)
    account_number = models.TextField(unique=True)
    account_name = models.TextField(null=True, blank=True)
    created_dts = models.DateTimeField(auto_now=True)
    open_date = models.DateTimeField(auto_now=True)
    close_date = models.DateTimeField(null=True, blank=True)
    status = models.TextField()
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.TextField()
    
    class Meta:
        db_table = "accounts"
        managed = True

    def __str__(self):
        return f"{self.account_number} ({self.currency})"
    
class CustomerAccount(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                 db_column="customer_id")
    account = models.ForeignKey('Account', on_delete=models.CASCADE,
                                db_column='account_id')

    class Meta:
        db_table = "customer_accounts"
        unique_together = ('customer', 'account')
        managed = True

class CurrencyQuote(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('CNY', 'Юань'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    value = models.DecimalField(max_digits=12, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'currency_quotes'
        verbose_name = 'Котировка валюты'
        verbose_name_plural = 'Котировки валют'

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Снятие'),
        ('transfer', 'Перевод'),
    ]
    transaction_date = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='account_id', related_name='transactions')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    another_account = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'