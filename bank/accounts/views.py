from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import *
from accounts.serializers import *
from django.db import connection
from rest_framework.views import APIView
from django.db.models import Max
import random
from datetime import datetime

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        customer = Customer.objects.get(email=request.user.email)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

class AccountViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return Response([])
        account_links = CustomerAccount.objects.filter(customer=customer)
        accounts = Account.objects.filter(account_id__in=account_links.values_list('account_id', flat=True))
        serializer = self.get_serializer(accounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='lookup', permission_classes=[AllowAny], url_name='account-lookup')
    def lookup(self, request):
        account_number = request.query_params.get('account_number')
        if not account_number or len(account_number) != 16 or not account_number.isdigit():
            return Response({'error': 'Invalid account number'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the Account by number
            account = Account.objects.get(account_number=account_number)
            # Find the Customer linked to this Account
            customer_account = CustomerAccount.objects.get(account=account)
            customer = customer_account.customer
            # Return customer's name
            return Response({'name': f'{customer.first_name} {customer.last_name}'})
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except CustomerAccount.DoesNotExist:
             return Response({'error': 'Customer not linked to account'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in account lookup: {e}")
            return Response({'error': 'An internal error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            customer = Customer.objects.get(email=user.email)
        except Customer.DoesNotExist:
            return Response({'error': 'Для пользователя не найден профиль клиента (Customer).'}, status=400)
        
        data = request.data
        currency = data.get('currency', 'RUB')
        status_ = data.get('status', 'active')
        balance = data.get('balance', 0)
        account_name = data.get('account_name', 'Платёжный счёт')

        # Generate a unique 16-digit account number
        # Format: 40702XXXXXXXXXXXX where X is a random digit
        while True:
            # Generate random part
            random_part = ''.join([str(random.randint(0, 9)) for _ in range(11)])
            # Combine with prefix
            account_number = f"40702{random_part}"
            if not Account.objects.filter(account_number=account_number).exists():
                break

        # Create the account
        account = Account.objects.create(
            account_number=account_number,
            status=status_,
            balance=balance,
            currency=currency,
            account_name=account_name
        )

        # Create the customer-account link
        CustomerAccount.objects.create(customer=customer, account=account)
        
        serializer = self.get_serializer(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuotesAPIView(APIView):
    def get(self, request):
        latest = (
            CurrencyQuote.objects
            .values('currency')
            .annotate(latest_update=Max('updated_at'))
        )
        result = []
        for item in latest:
            quote = CurrencyQuote.objects.filter(currency=item['currency'], updated_at=item['latest_update']).first()
            if quote:
                result.append(CurrencyQuoteSerializer(quote).data)
        return Response(result)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        account_id = self.request.query_params.get('account_id')
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        return queryset.order_by('-transaction_date')
    
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

class DepositAPIView(APIView):
    permission_classes = [IsAuthenticated]
    print('DepositAPIView')
    
    def post(self, request):
        print("Request data:", request.data)
        serializer = DepositSerializer(data=request.data)
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        account_id = serializer.validated_data['account_id']
        amount = serializer.validated_data['amount']
        
        try:
            with transaction.atomic():
                # Здесь ошибка в коде - у Account нет поля user, нужно использовать CustomerAccount
                customer = Customer.objects.get(user=request.user)
                account = Account.objects.select_for_update().get(
                    account_id=account_id
                )
                # Проверяем, что счет принадлежит клиенту
                CustomerAccount.objects.get(customer=customer, account=account)
                
                # Пополнение счёта
                account.balance += amount
                account.save()
                
                # Создание записи о транзакции
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='DEPOSIT',
                    transaction_date=datetime.now(),
                    description=f"Пополнение счёта на {amount} {account.currency}"
                )
                
                return Response(
                    AccountSerializer(account).data,
                    status=status.HTTP_200_OK
                )
                
        except (Account.DoesNotExist, CustomerAccount.DoesNotExist):
            return Response(
                {'error': 'Счёт не найден или вам не принадлежит'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        account_number = serializer.validated_data['account_number']
        another_account_number = serializer.validated_data['another_account_number']
        amount = serializer.validated_data['amount']

        print(account_number, another_account_number, amount)
        
        try:
            with transaction.atomic():
                # Получаем счёт отправителя
                sender_account = Account.objects.select_for_update().get(
                    account_number=account_number
                )
                customer = Customer.objects.get(user=request.user)
                # Проверяем, что счёт принадлежит клиенту
                CustomerAccount.objects.get(customer=customer, account=sender_account)

                # Получаем счёт получателя
                receiver_account = Account.objects.select_for_update().get(
                    account_number=another_account_number
                )

                if sender_account.currency == receiver_account.currency:
                    print('account.currency == another_account.currency')
                    if sender_account.balance >= amount:
                        # Пополнение счёта
                        sender_account.balance -= amount
                        sender_account.save()

                        receiver_account.balance += amount
                        receiver_account.save()
                        
                        # # Создание записи о транзакции
                        # Transaction.objects.create(
                        #     account_id=account.id,
                        #     another_account=another_account.id,
                        #     amount=amount,
                        #     transaction_type='TRANSFER',
                        #     transaction_date=datetime.now(),
                        #     description=f"Перевод {amount} {account.currency}"
                        # )
                    
                    return Response(
                        {
                            'message': 'Перевод выполнен успешно',
                            'sender_account': sender_account.account_number,
                            'receiver_account': receiver_account.account_number,
                            'amount': amount,
                            'currency': sender_account.currency
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': 'Невозможно совершить перевод: у счетов разная валюта'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                
        except (Account.DoesNotExist, CustomerAccount.DoesNotExist):
            return Response(
                {'error': 'Счёт не найден или вам не принадлежит'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )