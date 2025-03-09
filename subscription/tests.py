from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from subscription.models import Subscription

User = get_user_model()


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='alina@fob.ru',
                                             password='Poma2404')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="Advanced Django",
            description="An advanced course on Django framework.",
        )

    def test_add_subscription(self):
        """Тестирование добавления подписки"""
        # Проверяем, что подписки нет изначально
        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).count(), 0)

        response = self.client.post(reverse('subscription:subscribe', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'message': 'Subscription added.'})

        # Проверяем, что подписка теперь существует
        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).count(), 1)

    def test_remove_subscription(self):
        """Тестирование удаления подписки"""
        # Сначала добавляем подписку
        self.client.post(reverse('subscription:subscribe', kwargs={'course_id': self.course.id}))

        # Проверяем, что подписка существует
        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).count(), 1)

        # Теперь удаляем подписку
        response = self.client.post(reverse('subscription:subscribe', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Subscription removed.'})

        # Проверяем, что подписка была удалена
        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).count(), 0)
