from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )

    phone = models.CharField(
        max_length=35,
        verbose_name='Телефон',
        **NULLABLE
    )
    city = models.CharField(
        max_length=150,
        verbose_name='Город',
        **NULLABLE
    )
    avatar = models.ImageField(
        upload_to='images_users/',
        verbose_name='Аватарка',
        **NULLABLE
    )

    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
