import factory

from faker import Faker
from users.models import User
from factory.django import DjangoModelFactory

fake = Faker()


class UserFactory(DjangoModelFactory):
    """
    Фабрика для создания тестовых пользователей.
    """

    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Переопределяем метод создания пользователя,
        чтобы в качестве username использовать first_name.
        """

        manager = cls._get_manager(model_class)

        first_name = kwargs.pop('first_name', 'Test')
        last_name = kwargs.pop('last_name', 'User')
        email = kwargs.pop('email', f"{first_name}@example.com")

        return manager.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            *args,
            **kwargs
        )
