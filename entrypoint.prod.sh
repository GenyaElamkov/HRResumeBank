#!/bin/bash

# Ожидание доступности базы данных
echo "Waiting for database..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Database is ready!"

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn -c /app/gunicorn.conf.py core.project.wsgi:application