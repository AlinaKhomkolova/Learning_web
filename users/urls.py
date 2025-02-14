from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import UserViewSet, RegisterView, PaymentViewSet, PaymentCreateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(f'users', UserViewSet, basename='users')
router.register(f'payments_details', PaymentViewSet, basename='payments_details')

urlpatterns = [
                  # Регистрация маршрута для API, чтобы получить доступ к данным пользователя
                  path('api/', include(router.urls)),

                  # Эндпоинт для регистрации пользователя
                  path('register/', RegisterView.as_view(), name='register'),

                  # Эндпоинт для получения JWT-токена
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  # Эндпоинт для обновления JWT-токена
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                  # Эндпоинт для Strip-сессии оплаты
                  path('payment/', PaymentCreateAPIView.as_view(), name='payment')
              ] + router.urls
