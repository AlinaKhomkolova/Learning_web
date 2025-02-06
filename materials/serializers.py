from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import DescriptionValidator


class LessonSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True,
        validators=[DescriptionValidator(field='description')]
    )

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InfoLessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подробного отображения информации о курсе.
    Включает список уроков и их количество.
    """
    lessons = LessonSerializer(many=True, read_only=True)  # Сериализует все уроки
    number_of_lesson = SerializerMethodField()  # Поле для вывода количества уроков

    def get_number_of_lesson(self, course):
        """
        Метод для подсчета количества уроков в курсе.
        """
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'lessons', 'number_of_lesson')
