from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'session_id', 'payment_url', 'amount', 'user']


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)  # поле с платежами

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'token', 'payments', 'payment_details']
