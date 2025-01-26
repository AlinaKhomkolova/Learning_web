from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import UserViewSet, PayViewSet, RegisterView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(f'users', UserViewSet, basename='users')
router.register(f'payments', PayViewSet, basename='payments')

urlpatterns = [
                  # Регистрация маршрута для API, чтобы получить доступ к данным пользователя
                  path('api/', include(router.urls)),

                  path('register/', RegisterView.as_view(), name='register'),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
