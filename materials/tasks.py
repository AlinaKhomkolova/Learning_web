# courses/tasks.py
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from config import settings
from subscription.models import Subscription
from .models import Course


@shared_task
def send_course_update_email(course_id):
    """
    Асинхронная задача для отправки email-уведомлений пользователям, подписанным на обновления курса.
    """
    try:
        course = Course.objects.get(id=course_id)
        # Получаем всех пользователей, подписанных на курс через модель Subscription
        subscribers = Subscription.objects.filter(course=course)

        # Тема и текст письма
        subject = f"Обновление курса: {course.name}"
        message = f"Курс {course.name} был обновлен. Посмотрите новые материалы!"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Отправка письма всем подписанным пользователям
        for subscription in subscribers:
            user = subscription.user
            send_mail(subject, message, from_email, [user.email])

        return f"Рассылка для курса {course.name} завершена."

    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден."
