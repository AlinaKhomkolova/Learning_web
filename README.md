# Проект "Learning Web"

## Инструкция для развертывания проекта
### 1. Клонирование проекта
```bash
git clone git@github.com:AlinaKhomkolova/Learning_web.git
```

### 2. Создание и настройка окружения
Для работы с проектом используйте Docker. Не нужно устанавливать дополнительные зависимости вручную.

### 3. Настройка окружения
Создайте файл .env в корне проекта и добавьте необходимые переменные окружения. Пример содержимого файла .env:

```bazaar
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
REDIS_HOST=redis
REDIS_PORT=6379
```
Замените your_user, your_password, и your_db на реальные значения для вашего проекта.


### 4. Запуск проекта через Docker Compose
Для запуска всех сервисов проекта выполните команду:
```bash
sudo docker-compose up -d --build
```
Эта команда создаст и запустит контейнеры в фоновом режиме.

### 5. Проверка работоспособности сервисов
После успешного запуска проекта, можно проверить работоспособность каждого из сервисов.

#### 1. Web сервис (Django)
Веб-приложение будет доступно на порту 8000. Чтобы проверить его работоспособность, откройте браузер и перейдите по следующему адресу:
```bazaar
http://localhost:8000
```

#### 2. PostgreSQL
Для проверки работы базы данных PostgreSQL выполните команду для подключения к контейнеру базы данных:
```bash
sudo docker exec -it learning_web_db_1 psql -U your_user -d your_db
```
Если подключение прошло успешно, это значит, что сервис базы данных работает.

#### 3. Redis
Чтобы проверить работоспособность Redis, подключитесь к контейнеру Redis и выполните команду:
```bash
sudo docker exec -it learning_web_redis_1 redis-cli ping
```
Если Redis работает правильно, вы получите ответ:
```
PONG
```
#### 4. Celery
Для проверки работы Celery, выполните команду для просмотра логов Celery контейнера:
```bash
sudo docker logs learning_web_celery_1
```
Если контейнер Celery работает, в логах будет видно, что он запущен и слушает очередь задач.

#### 5. Celery Beat
Для проверки работы Celery Beat, который управляет периодическими задачами, проверьте логи:
```bash
sudo docker logs learning_web_celery_beat_1
```
Если всё настроено правильно, в логах появятся сообщения, связанные с выполнением задач по расписанию.

#### 6. Остановка и удаление контейнеров
Чтобы остановить все сервисы и удалить контейнеры, используйте команду:
```bash
sudo docker-compose down
```
Если нужно удалить также тома и сети, используйте:
```bash
sudo docker-compose down -v
```

Автор проекта
Хомколова Алина

