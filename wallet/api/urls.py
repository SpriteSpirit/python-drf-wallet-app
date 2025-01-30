from django.urls import path
from wallet.apps import WalletConfig


app_name = WalletConfig.name

urlpatterns = [
    path('', ..., name='wallet'),
]
