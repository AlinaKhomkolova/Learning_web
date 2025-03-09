import re

from rest_framework.exceptions import ValidationError


class DescriptionValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """
        Проверяет, содержит ли поле хотя бы одну ссылку на YouTube.
        """

        if not isinstance(value, str):
            raise ValidationError(f"Поле '{self.field}' должно содержать строку.")

        # Регулярное выражение для поиска ссылок на YouTube в тексте
        youtube_pattern = re.compile(r"https?://(www\.)?(youtube\.com|youtu\.be)/\S+")

        # Ищем ссылку в тексте
        if not youtube_pattern.search(value):
            raise ValidationError(f"Поле '{self.field}' должно содержать хотя бы одну ссылку на YouTube.")