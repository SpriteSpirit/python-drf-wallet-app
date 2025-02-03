import factory

from users.factories import UserFactory
from factory.django import DjangoModelFactory


class WalletFactory(DjangoModelFactory):
    """
    Фабрика для создания тестовых кошельков, связанных с пользователями.
    """

    class Meta:
        """
        Определяет модель Wallet, для которой создается фабрика.
        """

        model = 'wallet.Wallet'

    user = factory.SubFactory(UserFactory)
    balance = 100.00
