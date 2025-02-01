from rest_framework import serializers
from users.models import User
from wallet.api.serializers import WalletSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    """

    class Meta:
        """
        Метаданные сериализатора.
        """

        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

    def get_wallet(self, instance: User) -> dict:
        """
        Получает сериализованные данные кошелька пользователя.

        Если кошелек пользователя существует, возвращает его данные, иначе возвращает {}.
        Это позволит отключать кошелек при сериализации пользователей в API.

        Args:
        instance (User): Экземпляр модели пользователя.
        """

        if instance.wallet:
            return WalletSerializer(instance.wallet).data
        return {}
