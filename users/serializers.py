from rest_framework import serializers

from users.models import User, Pay


class PaySerializer(serializers.ModelSerializer):
    # Сериализатор для вывода данных платежа
    class Meta:
        model = Pay
        fields = ['id', 'data_pay', 'amount', 'payment_method', 'pay_course', 'pay_lesson']


class UserSerializer(serializers.ModelSerializer):
    payments = PaySerializer(many=True, read_only=True)  # поле с платежами

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'token', 'payments']
