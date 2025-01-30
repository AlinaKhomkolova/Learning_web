from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'image', 'course', 'owner')


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InfoLessonSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Вывод всех уроков
    number_of_lesson = SerializerMethodField()  # Вывод количества уроков

    def get_number_of_lesson(self, course):
        return course.lessons.count()  # Подсчет количества уроков для курса

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'lessons', 'number_of_lesson')
