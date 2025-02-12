from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from users.models import User, PaymentDetails, Payment
from users.paginators import UsersPagination
from users.serializers import UserSerializer, PaymentDetailsSerializer
from users.services import create_stripe_session, create_stripe_price, create_product


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
class PaymentDetailsFilter(FilterSet):
    """
    Класс фильтра для модели `PaymentDetails`.

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
        model = PaymentDetails
        fields = ['pay_course', 'pay_lesson', 'payment_method', ]


class PaymentDetailsViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с платежами.

    Этот класс позволяет обрабатывать запросы на создание, чтение, обновление и удаление
    данных о платежах. Также позволяет фильтровать платежи по курсу, уроку и способу оплаты.
    Сортировка осуществляется по дате оплаты по умолчанию.
    """
    serializer_class = PaymentDetailsSerializer

    # Настройка фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentDetailsFilter
    ordering_fields = ['data_pay']  # Поле для сортировки
    ordering = ['-data_pay']  # По умолчанию сортировка по дате оплаты(по убыванию)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # показывать только для текущего пользователя
        return PaymentDetails.objects.filter(user=self.request.user)


class PaymentCreateAPIView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        # Получаем данные о курсе или уроке из запроса
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)

        # Создаем продукт в Stripe
        try:
            product = create_product(course.name, course.description)
        except Exception as e:
            return Response({"error": f"Ошибка при создании продукта: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем цену в Stripe
        try:
            price = create_stripe_price(course.amount, product['id'])
        except Exception as e:
            return Response({"error": f"Ошибка при создании цены: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем сессию на оплату
        try:
            session_id, checkout_url = create_stripe_session(price['id'], success_url, cancel_url)
        except Exception as e:
            return Response({"error": f"Ошибка при создании сессии: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем объект Payment в нашей системе
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            session_id=session_id,
            checkout_url=checkout_url,
        )

        # Возвращаем ссылку на оплату в ответе
        return Response({
            "payment_url": checkout_url,
            "session_id": session_id
        }, status=status.HTTP_201_CREATED)


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
