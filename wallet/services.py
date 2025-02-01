from decimal import Decimal

from utilities.logger_utils import logger
from .models import Wallet
from django.db import transaction

@transaction.atomic
def perform_operation(wallet_id: str, operation_type: str, amount: Decimal) -> None:
    """
    Выполняет операцию над кошельком (пополнение или списание).

    Args:
        wallet_id (str): UUID кошелька.
        operation_type (str): Тип операции ("DEPOSIT" или "WITHDRAW").
        amount (Decimal): Сумма операции.

    :raises ValueError: Если тип операции неверный или недостаточно средств.
    """

    wallet = Wallet.objects.select_for_update().get(wallet_id=wallet_id)
    logger.info(f"Начат процесс обновления кошелька {wallet.wallet_id}. Текущий баланс: {wallet.balance}")

    if operation_type == "DEPOSIT":
        wallet.deposit(amount)
        logger.info(f"Кошелек {wallet.wallet_id} пополнен на {amount}. Новый баланс: {wallet.balance}")
    elif operation_type == "WITHDRAW":
        wallet.withdraw(amount)
        logger.info(f"С кошелька {wallet.wallet_id} списано {amount}. Новый баланс: {wallet.balance}")
    else:
        raise ValueError("Неверный тип операции.")