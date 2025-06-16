from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts import views
from accounts.auth import RegisterView, LoginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    # Include router URLs
    path('accounts/deposit/', views.DepositAPIView.as_view(), name='account-deposit'),
    path('accounts/transfer/', views.TransferAPIView.as_view(), name='account-deposit'),
    path('', include(router.urls)),  # This will be under /api/

    # Auth endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quotes/', views.QuotesAPIView.as_view(), name='quotes'),
    path('api-auth/', include('rest_framework.urls')),
    
]