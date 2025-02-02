from django.db import models
from django.db.models import Model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Модель пользователя.

    Attributes:
        email (EmailField): Адрес электронной почты. Уникальное поле.
        first_name (CharField): Имя пользователя.
        last_name (CharField): Фамилия пользователя. Может быть пустым.
    """

    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        """
         Метаданные для определения наименований модели и её поведения.
        """

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        """
        Возвращает строковое представление модели.
        """

        return f"{self.email}"


@receiver(post_save, sender=User)
def create_wallet(sender: type[Model], instance: User, created: bool, **kwargs) -> None:
    """
    При создании нового пользователя создает для него кошелек.

    Args:
        sender (type[Model]): Класс модели, который вызвал сигнал.
        instance (User): Созданный или измененный экземпляр модели.
        created (bool): Был ли создан новый экземпляр.
        kwargs (dict): Дополнительные параметры.
    """

    from wallet.models import Wallet

    if created:
        Wallet.objects.create(user=instance, balance=0.0)
