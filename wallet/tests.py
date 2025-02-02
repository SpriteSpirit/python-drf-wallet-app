from decimal import Decimal

from django.db import IntegrityError
from django.db.models.signals import post_save
from rest_framework.test import APITestCase  #, APIClient

from users.factories import UserFactory
from users.models import create_wallet, User
from utilities.logger_utils import logger

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

        logger.info("Начало теста test_unique_wallet_per_user")
        user = UserFactory()
        logger.debug(f"Создан пользователь с id: {user.id}")
        WalletFactory(user=user, balance=100.00)
        logger.debug(f"Создан кошелек для пользователя с id: {user.id}")

        with self.assertRaises(IntegrityError):
            logger.debug("Попытка создать второй кошелек для пользователя")
            WalletFactory(user=user, balance=50.00)
        logger.info("Тест test_unique_wallet_per_user пройден успешно")

    def test_deposit(self):
        """
        Тестирует операцию снятия средств с кошелька.
        """

        logger.info("Начало теста test_deposit")
        user = UserFactory()
        logger.debug(f"Создан пользователь с id: {user.id}")
        self.wallet = WalletFactory(user=user, balance=100.00)
        logger.debug(f"Создан кошелек для пользователя с id: {user.id} и балансом: {self.wallet.balance}")

        logger.debug("Выполняется операция DEPOSIT")
        perform_operation(self.wallet.wallet_id, "DEPOSIT", Decimal(50.00))

        self.wallet.refresh_from_db()
        logger.debug(f"Обновлен баланс кошелька: {self.wallet.balance}")
        self.assertEqual(self.wallet.balance, 150.00)
        logger.info("Тест test_deposit пройден успешно")

    def test_withdraw(self):
        """
        Тестирует случай, когда попытка снятия средств превышает доступный баланс.
        """

        logger.info("Начало теста test_withdraw")
        user = UserFactory()
        logger.debug(f"Создан пользователь с id: {user.id}")
        self.wallet = WalletFactory(user=user, balance=100.00)
        logger.debug(f"Создан кошелек для пользователя с id: {user.id} и балансом: {self.wallet.balance}")

        logger.debug("Выполняется операция WITHDRAW")
        perform_operation(self.wallet.wallet_id, "WITHDRAW", Decimal(50.00))

        self.wallet.refresh_from_db()
        logger.debug(f"Обновлен баланс кошелька: {self.wallet.balance}")
        self.assertEqual(self.wallet.balance, 50.00)
        logger.info("Тест test_withdraw пройден успешно")

    def test_insufficient_funds(self):
        """
        Тестирует случай, когда указывается недопустимый тип операции.
        """

        logger.info("Начало теста test_insufficient_funds")
        user = UserFactory()
        logger.debug(f"Создан пользователь с id: {user.id}")
        self.wallet = WalletFactory(user=user, balance=100.00)
        logger.debug(f"Создан кошелек для пользователя с id: {user.id} и балансом: {self.wallet.balance}")

        logger.debug("Попытка выполнить операцию WITHDRAW с превышением баланса")
        with self.assertRaises(ValueError):
            perform_operation(self.wallet.wallet_id, "WITHDRAW", Decimal(150.00))
        logger.info("Тест test_insufficient_funds пройден успешно")

    def test_invalid_operation_type(self):
        """
        Тестирует случай, когда указывается недопустимый тип операции.
        """

        logger.info("Начало теста test_invalid_operation_type")
        user = UserFactory()
        logger.debug(f"Создан пользователь с id: {user.id}")
        self.wallet = WalletFactory(user=user, balance=100.00)
        logger.debug(f"Создан кошелек для пользователя с id: {user.id} и балансом: {self.wallet.balance}")

        logger.debug("Попытка выполнить операцию с недопустимым типом")
        with self.assertRaises(ValueError):
            perform_operation(self.wallet.wallet_id, "INVALID", Decimal(50.00))
        logger.info("Тест test_invalid_operation_type пройден успешно")
