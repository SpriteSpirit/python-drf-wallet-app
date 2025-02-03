import uuid

from decimal import Decimal
from django.db import models


class Wallet(models.Model):
    """
    Модель кошелька, представляющая собой цифровой кошелек пользователя.

    Attributes:
        user (models.OneToOneField): Пользователь, которому принадлежит кошелек.
        balance (models.DecimalField): Текущий баланс кошелька.
        wallet_id (models.UUIDField): Уникальный идентификатор кошелька.
    """

    objects = models.Manager()

    user = models.OneToOneField('users.User',
                                on_delete=models.CASCADE,
                                verbose_name="Пользователь",
                                related_name='wallet')

    balance = models.DecimalField(max_digits=10,
                                  decimal_places=2,
                                  default=0.0,
                                  verbose_name="Баланс")

    wallet_id = models.UUIDField(unique=True,
                                 primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False,
                                 verbose_name="ID кошелька")

    class Meta:
        """
        Метаданные для определения наименований модели и её поведения.
        """

        # app_label = 'wallet'
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'


    def __str__(self) -> str:
        """
        Возвращает строковое представление модели.
        """

        return f'Кошелек id[{self.wallet_id}] пользователя {self.user.username}'

    def deposit(self, amount: Decimal) -> None:
        """
        Пополнение баланса.

        :param amount: Сумма пополнения.
        """

        self.balance += amount
        self.save()

    def withdraw(self, amount: Decimal) -> None:
        """
        Списание средств.

        :param amount: Сумма списания.
        :raises ValueError: Если на счету недостаточно средств.
        """

        if self.balance < amount:
            raise ValueError("Недостаточно средств на счете")

        self.balance -= amount
        self.save()
