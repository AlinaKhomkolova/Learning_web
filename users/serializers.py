from rest_framework import serializers

from materials.services import convert_currencies
from users.models import User, PaymentDetails, Payment
from users.services import create_stripe_price, create_stripe_session


class PaymentDetailsSerializer(serializers.ModelSerializer):
    """Сериализатор для данных об оплате"""

    class Meta:
        model = PaymentDetails
        fields = ['__all__']

    # def validate(self, data):
    #     """Проверяем, что указан либо курс, либо урок"""
    #     pay_course = data.get('pay_course')
    #     pay_lesson = data.get('pay_lesson')
    #
    #     if not pay_course and not pay_lesson:
    #         raise serializers.ValidationError(
    #             'Необходимо указать либо pay_course, либо pay_lesson'
    #         )
    #
    #     return data


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для самой оплаты (Stripe-сессия, ссылка, статус)"""
    payment_details = PaymentDetailsSerializer()
    amount = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def create(self, validated_data):
        """Создание платежа с учетом цены курса или урока"""

        payment_details_data = validated_data.pop('payment_details')

        pay_course = payment_details_data.get('pay_course')
        pay_lesson = payment_details_data.get('pay_lesson')

        # Определяем сумму оплаты
        if pay_course:
            amount = pay_course.price
        elif pay_lesson:
            amount = pay_lesson.price
        else:
            raise serializers.ValidationError("Не удалось определить сумму оплаты.")

        # Создаем запись PaymentDetails
        payment_details = PaymentDetails.objects.create(
            user=self.context['request'].user,  # Беру пользователя из запроса
            pay_course=pay_course,
            pay_lesson=pay_lesson,
            amount=amount,
            payment_method=payment_details_data.get("payment_method", "cash")
        )

        # Создаю платеж
        payment = Payment.objects.create(payment_details=payment_details)

        # Конвертация суммы и создание Stripe-сессии
        amount_in_dollars = convert_currencies(amount)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_session(price)

        # Сохраняю данные Stripe в платеж
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

        return payment

    class Meta:
        model = Payment
        fields = ['id', 'session_id', 'link', 'amount', 'user', 'payment_details']


class UserSerializer(serializers.ModelSerializer):
    payments_detail = PaymentDetailsSerializer(many=True, read_only=True)  # поле с платежами

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'token', 'payments', 'payment_details']
