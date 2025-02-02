from decimal import Decimal

from django.db import IntegrityError
from django.db.models.signals import post_save
from rest_framework.test import APITestCase #, APIClient

from users.factories import UserFactory
from users.models import create_wallet, User

from wallet.factories import WalletFactory
from wallet.services import perform_operation


class WalletServiceTests(APITestCase):
    """
    Тесты для сервиса операций с кошельком.
    """

    @classmethod
    def setUpClass(cls):
        """
        Отключение сигнала post_save для создания кошелька после создания пользователя.
        """

        super().setUpClass()
        post_save.disconnect(create_wallet, sender=User)

    @classmethod
    def tearDownClass(cls):
        """
        Подключение сигнала после завершения набора тестов, чтобы предотвратить ненужные операции с базой данных.
        """

        post_save.connect(create_wallet, sender=User)
        super().tearDownClass()

    def setUp(self):
        """
        Настройка тестового окружения.
        """

        self.user = UserFactory()
        # для jwt авторизации
        # self.client = APIClient()
        # self.client.force_login(user=self.user)

    def test_unique_wallet_per_user(self):
        """
        Тестирует, что при создании второго кошелька для того же пользователя возникает ошибка IntegrityError.
        """

        user = UserFactory()  # Create user
        WalletFactory(user=user, balance=100.00)
        with self.assertRaises(IntegrityError):
            WalletFactory(user=user, balance=50.00)


    def test_deposit(self):
        """
        Тестирует операцию снятия средств с кошелька.
        """

        user = UserFactory()  # Create user
        self.wallet = WalletFactory(user=user, balance=100.00)
        perform_operation(self.wallet.wallet_id, "DEPOSIT", Decimal(50.00))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 150.00)


    def test_withdraw(self):
        """
        Тестирует случай, когда попытка снятия средств превышает доступный баланс.
        """

        user = UserFactory()  # Create user
        self.wallet = WalletFactory(user=user, balance=100.00)
        perform_operation(self.wallet.wallet_id, "WITHDRAW", Decimal(50.00))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 50.00)


    def test_insufficient_funds(self):
        """
        Тестирует случай, когда указывается недопустимый тип операции.
        """

        user = UserFactory()  # Create user
        self.wallet = WalletFactory(user=user, balance=100.00)
        with self.assertRaises(ValueError):
            perform_operation(self.wallet.wallet_id, "WITHDRAW", Decimal(150.00))


    def test_invalid_operation_type(self):
        """

        """

        user = UserFactory()  # Create user
        self.wallet = WalletFactory(user=user, balance=100.00)
        with self.assertRaises(ValueError):
            perform_operation(self.wallet.wallet_id, "INVALID", Decimal(50.00))