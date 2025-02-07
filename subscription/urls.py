from django.urls import path

from subscription.apps import SubscriptionConfig
from subscription.views import SubscriptionView

app_name = SubscriptionConfig.name

urlpatterns = [
    path('subscribe/<int:course_id>/', SubscriptionView.as_view(), name='subscribe'),  # Эндпоинт для подписки
]
