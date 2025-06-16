from rest_framework import serializers
from .models import Customer, Account, CurrencyQuote, Transaction
from django.contrib.auth.models import User
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['customer_id']
        extra_kwargs = {
            'customer_id': {'required': False},
            'birth_date': {'required': False},
            'tax_id': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False}
        }

    def create(self, validated_data):
        # Удаляем password из данных, так как он не нужен для создания Customer
        validated_data.pop('password', None)
        
        # Generate a unique customer_id
        validated_data['customer_id'] = int(str(uuid.uuid4().int)[:10])  # Generate a 10-digit number
        return super().create(validated_data)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class CurrencyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyQuote
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class DepositSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

class TransferSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    another_account_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)