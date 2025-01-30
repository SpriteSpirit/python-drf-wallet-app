from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Модель пользователя.

    Attributes:
        email (EmailField): Адрес электронной почты. Уникальное поле.
        first_name (CharField): Имя пользователя.
        last_name (CharField): Фамилия пользователя. Может быть пустым.
        wallet_id (CharField): ID кошелька пользователя.
    """

    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)
    wallet_id = models.CharField(max_length=50, verbose_name='Wallet ID')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
