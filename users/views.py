from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from materials.models import Course, Lesson
from users.models import User, Pay
from users.serializers import UserSerializer, PaySerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# Настройка фильтров
class PayFilter(FilterSet):
    pay_course = ModelChoiceFilter(
        queryset=Course.objects.all(),
        field_name='pay_course',
        label='Фильтр по курсу'
    )
    pay_lesson = ModelChoiceFilter(
        queryset=Lesson.objects.all(),
        field_name='pay_lesson',
        label='Фильтр по уроку'
    )
    payment_method = CharFilter(
        lookup_expr='iexact',  # Способ поиска для фильтров.
        field_name='payment_method',
        label='Фильтр по способу оплаты'
    )

    class Meta:
        model = Pay
        fields = ['pay_course', 'pay_lesson', 'payment_method', ]


class PayViewSet(viewsets.ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer

    # Настройка фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PayFilter
    ordering_fields = ['data_pay']  # Поле для сортировки
    ordering = ['-data_pay']  # По умолчанию сортировка по дате оплаты(по убыванию)
