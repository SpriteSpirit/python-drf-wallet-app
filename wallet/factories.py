import factory
from factory.django import DjangoModelFactory
from users.factories import UserFactory


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