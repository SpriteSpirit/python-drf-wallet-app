from django.urls import path

from wallet.apps import WalletConfig
from wallet.api.views import WalletViewSet


app_name = WalletConfig.name

urlpatterns = [
    # GET api/v1/wallets
    path('', WalletViewSet.as_view({'get': 'list'}), name='wallet-list'),
    # GET api/v1/wallets/<WALLET_UUID>
    path('<uuid:wallet_id>/', WalletViewSet.as_view({'get': 'retrieve'}), name='wallet-detail'),
    # GET api/v1/wallets/<WALLET_UUID>/info
    path('<uuid:wallet_id>/info/', WalletViewSet.as_view({'get': 'info'}), name='wallet-balance'),
    # POST api/v1/wallets/<WALLET_UUID>/operation
    path('<uuid:wallet_id>/operation/', WalletViewSet.as_view({'post': 'operation'}), name='wallet-operation'),
]
