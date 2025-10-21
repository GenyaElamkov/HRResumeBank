#!/bin/bash

# Ожидание доступности базы данных
echo "Waiting for database..."
# while ! nc -z postgres2 5432; do
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Database is ready!"

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate --noinput

# Сбор статических файлов (ВАЖНО для production!)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Создание суперпользователя (опционально, для разработки)
# echo "Creating superuser..."
# python manage.py createsuperuser --noinput || true

echo "Starting Gunicorn..."
exec gunicorn -c /app/gunicorn.conf.py core.project.wsgi:application