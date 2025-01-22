from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PayViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(f'users', UserViewSet, basename='users')
router.register(f'payments', PayViewSet, basename='payments')

urlpatterns = [

              ] + router.urls
