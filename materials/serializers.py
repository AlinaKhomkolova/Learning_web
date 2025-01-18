from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class NumberCourseSerializer(ModelSerializer):
    number_course = SerializerMethodField()

    def get_number_course(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'number_course')


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
