from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson

User = get_user_model()


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='alina@fob.ru',
                                             password='Poma2404')
        self.client.force_authenticate(user=self.user)

        # Создание курса
        self.course = Course.objects.create(
            name="Advanced Django",
            description="An advanced course on Django framework.",
        )

        # Создание уроков
        self.lesson1 = Lesson.objects.create(
            name="Lesson 1",
            description="Introduction to Django",
            course=self.course,
            image=None,
            owner=None
        )

        self.lesson2 = Lesson.objects.create(
            name="Lesson 2",
            description="Models and ORM",
            course=self.course,
            image=None,
            owner=None
        )

        self.course.number_of_lesson = self.course.lessons.count()
        self.course.save()

    def test_create_course(self):
        """Тестирование создания курса"""

        data = {
            'name': 'Django course',
            'description': 'Django laerning description',
        }
        response = self.client.post('/course/', data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(response.json(),
                         {'id': 2, 'name': 'Django course',
                          'description': 'Django laerning description',
                          'is_subscribed': False},
                         {'id': 3, 'name': 'Python course',
                          'description': 'Ссылка на источник https://www.youtube.com/',
                          'is_subscribed': True}
                         )

        self.assertTrue(
            Course.objects.all().exists())

    def test_list_course(self):
        """Тестирование вывода списка курсов"""

        response = self.client.get('/course/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        courses = response.data['results']
        expected_data = [
            {
                'id': self.course.id,
                'name': self.course.name,
                'description': self.course.description,
                'is_subscribed': False,

            }
        ]
        self.assertEqual(courses, expected_data)

    def test_retrieve_course(self):
        """тестирование получения конкретного курса"""

        response = self.client.get(f'/course/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.course.id,
            'name': self.course.name,
            'description': self.course.description,
            'lessons': [
                {'id': self.lesson1.id, 'name': self.lesson1.name, 'description': self.lesson1.description,
                 'image': None, 'course': self.course.id, 'owner': None},
                {'id': self.lesson2.id, 'name': self.lesson2.name, 'description': self.lesson2.description,
                 'image': None, 'course': self.course.id, 'owner': None},
            ],
            'number_of_lesson': 2,
            'is_subscribed': False,
        }

        self.assertEqual(response.json(), expected_data)

    def test_update_course(self):
        """Тестирование изменения курса"""
        data = {
            'name': 'Test update',
            'description': 'Test update desc'
        }
        response = self.client.put(f'/course/{self.course.id}/', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.course.refresh_from_db()
        self.assertEqual(self.course.name, 'Test update')
        self.assertEqual(self.course.description, 'Test update desc')

    def test_delete_course(self):
        """Тестирование удаления курса"""

        response = self.client.delete(f'/course/{self.course.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())




