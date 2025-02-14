from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import DescriptionValidator
from subscription.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True,
        validators=[DescriptionValidator(field='description')]
    )

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()  # Поле вывода подписки
    usd_price = serializers.SerializerMethodField()  # Поле вывода прайса в USD

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'is_subscribed', 'amount', 'usd_price']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user  # Получаем пользователя из контекста
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()  # Проверяем, есть ли подписка на курс
        return False


class InfoLessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подробного отображения информации о курсе.
    Включает список уроков и их количество.
    """
    lessons = LessonSerializer(many=True, read_only=True)  # Сериализует все уроки
    number_of_lesson = SerializerMethodField()  # Поле для вывода количества уроков
    is_subscribed = SerializerMethodField()  # Поле для подписки на курс

    def get_number_of_lesson(self, course):
        """
        Метод для подсчета количества уроков в курсе.
        """
        return course.lessons.count()

    def get_is_subscribed(self, course):
        """
        Метод для получения состояния подписки на курс для текущего пользователя.
        """
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=course).exists()
        return False

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'lessons', 'number_of_lesson', 'is_subscribed')
