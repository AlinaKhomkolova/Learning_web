from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не заходили в систему больше месяца.
    """
    one_month_ago = timezone.now() - timedelta(minutes=5)
    inactive_users = User.objects.filter(last_login__lte=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.email} был деактивирован из-за неактивности.")
