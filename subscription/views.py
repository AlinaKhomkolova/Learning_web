from rest_framework import status  # Добавьте этот импорт
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from subscription.models import Subscription


class SubscriptionView(APIView):

    def post(self, request, course_id):
        user = request.user  # Получаем текущего пользователя
        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        course = get_object_or_404(Course, id=course_id)
        subscription_exists = Subscription.objects.filter(user=user, course=course).exists()

        if subscription_exists:
            # Если подписка уже существует, удаляем её
            Subscription.objects.filter(user=user, course=course).delete()
            return Response({"message": "Subscription removed."}, status=status.HTTP_200_OK)
        else:
            # Если подписки нет, создаем новую
            Subscription.objects.create(user=user, course=course)
            return Response({"message": "Subscription added."}, status=status.HTTP_201_CREATED)
