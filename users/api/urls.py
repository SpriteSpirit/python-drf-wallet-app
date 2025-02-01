from users.apps import UsersConfig
from users.api.views import UserViewSet
from rest_framework.routers import DefaultRouter


app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = router.urls
