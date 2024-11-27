#!/bin/sh

sleep 60

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@um6p.ma', 'admin')

User.objects.create_user('user', 'user@um6p.ma', 'user')
User.objects.create_user('imad.kissami', 'imad.kissami@um6p.ma', 'imad.kissami')
User.objects.create_user('fahd.kalloubi', 'fahd.kalloubi@um6p.ma', 'fahd.kalloubi')
User.objects.create_user('hamza.lachkar', 'hamza.lachkar@um6p.ma', 'hamza.lachkar')
User.objects.create_user('haitham.naciri', 'haitham.naciri@um6p.ma', 'haitham.naciri')
User.objects.create_user('abdessamad.laamimi', 'abdessamad.laamimi@um6p.ma', 'abdessamad.laamimi')
EOF


# Start Django server
# gunicorn backend.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
