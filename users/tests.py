from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.factories import UserFactory


class UserViewSetTestCase(APITestCase):
    """
    Тесты для UserViewSet.
    """

    def test_create_user(self):
        """
        Тестирует создание нового пользователя.
        """

        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        response = self.client.post('/api/v1/users/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_factory(self):
        """
        Тестирует создание нового пользователя с помощью фабрики.
        """

        user = UserFactory()

        self.assertIsNotNone(user.id)
        self.assertRegex(user.email, r'^user\d+@example\.com$')

    def test_create_user_with_custom_email(self):
        """
        Тестирует создание нового пользователя с кастомным email.
        """

        user = UserFactory(email='custom@example.com')

        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, 'custom@example.com')
