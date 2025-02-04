from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal

from django.http import Http404

from wallet.models import Wallet
from utilities.logger_utils import logger


@transaction.atomic
def perform_operation(wallet_id: str, operation_type: str, amount: Decimal) -> Wallet:
    """
    Выполняет операцию над кошельком (пополнение или списание).

    Args:
        wallet_id (str): UUID кошелька.
        operation_type (str): Тип операции ("DEPOSIT" или "WITHDRAW").
        amount (Decimal): Сумма операции.

    :raises ValueError: Если тип операции неверный или недостаточно средств.
    :raises Http404: Если кошелек не найден.
    """

    try:
        wallet = Wallet.objects.select_for_update().get(wallet_id=wallet_id)
    except ObjectDoesNotExist:
        raise Http404(f"Кошелек с ID {wallet_id} не найден.")

    logger.info(f"Начат процесс операций с кошельком {wallet.wallet_id}. Текущий баланс: {wallet.balance}")

    if operation_type == "DEPOSIT":
        wallet.deposit(amount)
        logger.info(f"Кошелек {wallet.wallet_id} пополнен на {amount}. Новый баланс: {wallet.balance}")
        return wallet
    elif operation_type == "WITHDRAW":
        wallet.withdraw(amount)
        logger.info(f"С кошелька {wallet.wallet_id} списано {amount}. Новый баланс: {wallet.balance}")
        return wallet
    else:
        raise ValueError("Неверный тип операции.")
