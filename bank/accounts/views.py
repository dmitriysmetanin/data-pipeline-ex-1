from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import Customer, Account, CustomerAccount, CurrencyQuote, Transaction
from accounts.serializers import CustomerSerializer, AccountSerializer, CurrencyQuoteSerializer, TransactionSerializer
from django.db import connection
from rest_framework.views import APIView
from django.db.models import Max
import random

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