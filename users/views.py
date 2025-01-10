from rest_framework import viewsets

from users.serializers import UserSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
