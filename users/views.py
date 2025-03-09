from django.shortcuts import get_object_or_404
from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from users.models import User, Payment
from users.paginators import UsersPagination
from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_product, create_price, create_checkout_session


class UserViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с пользователями.

    Обрабатывает запросы на создание, чтение, обновление и удаление данных пользователя.
    Доступ только для аутентифицированных пользователей. В качестве фильтрации используется
    только информация о текущем пользователе.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # Ограничение, чтобы выводились только данный для текущего пользователя
    permission_classes = [IsAuthenticated]
    # Пагинация данных
    pagination_class = UsersPagination

    def get_queryset(self):
        """
        Возвращает только текущего пользователя в качестве queryset.

        Это используется для ограничения доступа к данным только для аутентифицированного пользователя.
        """
        return User.objects.filter(id=self.request.user.id)


# Настройка фильтров
class PaymentFilter(FilterSet):
    """
    Класс фильтра для модели `Payment`.

    Фильтрует данные о платежах по курсу, уроку и способу оплаты.
    """
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
        model = Payment
        fields = ['pay_course', 'pay_lesson', 'payment_method', ]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с платежами.

    Этот класс позволяет обрабатывать запросы на создание, чтение, обновление и удаление
    данных о платежах. Также позволяет фильтровать платежи по курсу, уроку и способу оплаты.
    Сортировка осуществляется по дате оплаты по умолчанию.
    """
    serializer_class = PaymentSerializer

    # Настройка фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['data_pay']  # Поле для сортировки
    ordering = ['-data_pay']  # По умолчанию сортировка по дате оплаты(по убыванию)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # показывать только для текущего пользователя
        return Payment.objects.filter(user=self.request.user)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        payment_method = request.data.get("payment_method")
        course_id = request.data.get("pay_course")
        lesson_id = request.data.get("pay_lesson")

        # Проверяем, что именно оплачивается
        if course_id:
            product = get_object_or_404(Course, id=course_id)
        elif lesson_id:
            product = get_object_or_404(Lesson, id=lesson_id)
        else:
            return Response({"error": "Не указан курс или урок"}, status=400)

        # Проверяем, что метод оплаты указан
        if not payment_method:
            return Response({"error": "Не указан метод оплаты"}, status=400)

        # Создаём продукт и цену в Stripe
        stripe_product_id = create_product(product.name, product.description)
        stripe_price_id = create_price(product.amount, stripe_product_id)

        # Если не удалось создать прайс, возвращаем ошибку
        if not stripe_price_id:
            return Response({"error": "Ошибка при создании цены в Stripe"}, status=500)

        # Создаем сессию оплаты
        session_id, session_url = create_checkout_session(stripe_price_id)

        # Если не удалось создать сессию, возвращаем ошибку
        if not session_id:
            return Response({"error": "Ошибка при создании сессии оплаты в Stripe"}, status=500)

        # Сохраняем в БД
        payment = Payment.objects.create(
            user=user,
            pay_course=product if isinstance(product, Course) else None,
            pay_lesson=product if isinstance(product, Lesson) else None,
            amount=product.amount,
            payment_method=payment_method,
            session_id=session_id,
            link=session_url
        )

        return Response(
            {
                "id": payment.id,
                "session_id": payment.session_id,
                "link": payment.link,
                "amount": payment.amount,
                "user": payment.user.email,
            },
            status=201
        )


class RegisterView(APIView):
    """
    Представление для регистрации нового пользователя.
    Это представление позволяет создать нового пользователя в системе. Доступ без аутентификации.
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # Это отключает JWT-аутентификацию для этого представления

    def post(self, request):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.

        Данные пользователя проходят валидацию через сериализатор `UserSerializer`.
        При успешной валидации, создается новый пользователь и возвращается успешный ответ.
        При неудаче возвращаются ошибки валидации.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
