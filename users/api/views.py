from users.models import User
from rest_framework import viewsets
from users.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления пользователями.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
