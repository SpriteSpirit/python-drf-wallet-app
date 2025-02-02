from decimal import Decimal
from typing import Optional
from wallet.models import Wallet
from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели кошелька.
    """

    class Meta:
        """
        Метаданные сериализатора.
        """

        model = Wallet
        fields = ['wallet_id', 'user', 'balance']


class WalletOperationSerializer(serializers.Serializer):
    """
    Сериализатор для валидации данных операции (operationType и amount).
    """

    operation_type = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.DecimalField(min_value=Decimal('0.01'), max_digits=10, decimal_places=2)

    def validate_amount(self, value: float) -> Optional[float]:
        """
        Проверка суммы на положительное значение.
        """

        if value < 0:
            raise serializers.ValidationError("Сумма должна быть положительной.")
        return value
