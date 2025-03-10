from django.db import models

from config import settings
from config.settings import NULLABLE


class Course(models.Model):
    """Курсы"""
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        help_text='Укажите название курса.'
    )
    image = models.ImageField(
        upload_to='images_course/',
        verbose_name='Изображение (превью)',
        help_text='Прикрепите изображение для превью.',
        **NULLABLE
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Добавьте подробное описание курса.',
        **NULLABLE)

    amount = models.IntegerField(
        default=1,
        verbose_name='Цена',
        help_text='Укажите цену в рублях',
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )

    last_updated_course = models.DateTimeField(auto_now=True, verbose_name='дата Последнего обновление')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Уроки"""
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        help_text='Укажите название урока.'
    )
    image = models.ImageField(
        upload_to='images_course/',
        verbose_name='Изображение (превью)',
        help_text='Прикрепите изображение для превью.',
        **NULLABLE
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Добавьте описание урока.',
        **NULLABLE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
        help_text='Укажите, к какому курсу относится этот урок.'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        **NULLABLE
    )
    amount = models.IntegerField(
        default=1,
        verbose_name='Цена',
        help_text='Укажите цену в рублях',
    )

    last_updated_lesson = models.DateTimeField(auto_now=True, verbose_name='дата Последнего обновление')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
