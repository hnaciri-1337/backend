#!/bin/sh

sleep 5

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ma.ma', 'admin')
    User.objects.create_user('user', 'user@ma.ma', 'user')
EOF


# Start Django server
# gunicorn backend.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
