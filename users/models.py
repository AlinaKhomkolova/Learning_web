from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import URLField

from config.settings import NULLABLE
from materials.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Пользователи, которые могут оплатить курс или урок.
    """
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

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def username(self):
        return self.get_username()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    """
    Данные об оплате
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь',
        help_text='Пользователь, который осуществил покупку.'
    )
    data_pay = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оплаты',
        help_text='Дата и время совершения оплаты.'
    )
    pay_course = models.ForeignKey(
        Course,
        **NULLABLE,
        on_delete=models.CASCADE,
        related_name='payments_for_course',
        verbose_name='Оплаченный курс',
        help_text='Курс, за который была произведена оплата.'
    )
    pay_lesson = models.ForeignKey(
        Lesson,
        **NULLABLE,
        on_delete=models.CASCADE,
        related_name='payments_for_lesson',
        verbose_name='Оплаченный урок',
        help_text='Урок, за который была произведена оплата.'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты',
        help_text='Сумма, которую заплатил пользователь.',
        default=1
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        verbose_name='Способ оплаты',
        help_text='Способ, с помощью которого была произведена оплата.'
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name='ID сессии',
        help_text='Укажите id сессии',
        **NULLABLE
    )
    link = URLField(
        max_length=400,
        verbose_name='Ссылка на оплату',
        help_text='Укажите ссылку на оплату',
        **NULLABLE
    )

    def __str__(self):
        return f"Оплата {self.amount} за {self.pay_course or self.pay_lesson}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'
