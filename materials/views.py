from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import MaterialsPagination
from materials.permissions import IsOwnerOrStaff
from materials.serializers import CourseSerializer, LessonSerializer, InfoLessonSerializer
from materials.tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    Доступ:
    - IsAuthenticated
    - IsOwnerOrStaff

    Методы:
    - list(),  retrieve(), create(), update(), destroy().
    """
    queryset = Course.objects.all().order_by('id')  # Сортировка по id
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    pagination_class = MaterialsPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        """
        Возвращает нужный сериализатор в зависимости от типа запроса.
        
        - 'retrieve' (Детальный просмотр) 'InfoLessonSerializer'
        - Остальные запросы 'CourseSerializer'
        """
        if self.action == 'retrieve':  # Для подробного отображения уроков
            return InfoLessonSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        При создании курса автоматически назначает владельца текущего пользователя
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Переопределяем метод обновления, чтобы после обновления курса отправить email
        подписанным пользователям
        """
        # Сохраняем изменения курса
        course = serializer.save()

        # Отправляем email всем подписанным на курс пользователям
        send_course_update_email.delay(course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    API для создания уроков.
    
    Доступ:
    - IsAuthenticated

    Метод:
    - create()
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        При создании урока автоматически назначает владельца текущего пользователя
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    API для получения списка уроков.

    Доступ:
    - IsAuthenticated

    Метод:
    - list()
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

    def get_queryset(self):
        """
        Возвращает список уроков:
        - Если пользователь — модератор, он видит все уроки.
        - Если обычный пользователь, он видит только свои уроки.
        """
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """        
    API для получения одного урока.
    
    Доступ:
    - Только владелец урока или администратор.
        
    Метод:
    - `retrieve()`
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    API для обновления урока.
    
    Доступ:
    - Только владелец урока или администратор.
        
    Метод:
    - `update()`
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления урока.
    
    Доступ:
    - Только владелец урока или администратор.
        
    Метод:
    - `destroy()`
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]
