from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.factories import UserFactory
from utilities.logger_utils import logger


class UserViewSetTestCase(APITestCase):
    """
    Тесты для UserViewSet.
    """

    def test_create_user(self):
        """
        Тестирует создание нового пользователя.
        """

        logger.info("Начало теста test_create_user")

        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        logger.debug(f"Отправка запроса на создание пользователя с данными: {user_data}")
        response = self.client.post('/api/v1/users/', user_data, format='json')
        logger.debug(f"Получен ответ от сервера: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        logger.info("Тест test_create_user пройден успешно")

    def test_create_user_with_factory(self):
        """
        Тестирует создание нового пользователя с помощью фабрики.
        """

        logger.info("Начало теста test_create_user_with_factory")
        user = UserFactory()

        logger.debug(f"Создан пользователь с id: {user.id} и email: {user.email}")
        self.assertIsNotNone(user.id)
        self.assertRegex(user.email, r'^user\d+@example\.com$')
        logger.info("Тест test_create_user_with_factory пройден успешно")

    def test_create_user_with_custom_email(self):
        """
        Тестирует создание нового пользователя с кастомным email.
        """

        logger.info("Начало теста test_create_user_with_custom_email")
        user = UserFactory(email='custom@example.com')

        logger.debug(f"Создан пользователь с id: {user.id} и email: {user.email}")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, 'custom@example.com')
        logger.info("Тест test_create_user_with_custom_email пройден успешно")
