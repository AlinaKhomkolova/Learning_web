from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    """
    Разрешение, позволяющее доступ только владельцу объекта или администратору.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право доступа к объекту.

        - Администратор всегда имеет доступ.
        - Любой аутентифицированный пользователь может создавать (`POST`).
        """

        if request.user.is_staff:
            # Разрешаем доступ администратору
            return True

        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        return True  # Разрешаю доступ к списку объектов (GET /course/)

    def has_objects_permission(self, request, obj):
        """Проверяем доступ к определенному объекту"""
        if request.user.is_staff:
            return True  # Администратор имеет доступ
        # Разрешаем доступ владельцу объекта
        return request.user == obj.owner
