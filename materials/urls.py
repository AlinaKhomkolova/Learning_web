from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(f'course', CourseViewSet, basename='course')
router.register(f'lesson', LessonViewSet, basename='lesson')

urlpatterns = [

              ] + router.urls
