FROM python:3.10-slim

# Устонавливаем рабочую директорию в контейнере
WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимосятми и устонавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

ENV ALLOWED_HOSTS="*"
ENV DEBUG="True"
ENV CELERY_BROKER_URL="redis://localhost:6379/0"
ENV CELERY_RESULT_BACKEND="redis://localhost:6379/0"

RUN mkdir -p app/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Команда запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]