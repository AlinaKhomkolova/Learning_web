import os

from celery import Celery
from celery.schedules import crontab

from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Используем настройки из конфигурации Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически регистрируем все задачи из всех приложений Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Настройка периодического расписания с использованием celery-beat
app.conf.beat_schedule = {
    'deactivate-inactive-users': {
        'task': 'users.tasks.deactivate_inactive_users',  # Путь к задаче
        'schedule': crontab(minute=0, hour=0),  # Выполняется каждый день в полночь
    },
}

app.conf.timezone = 'UTC'
