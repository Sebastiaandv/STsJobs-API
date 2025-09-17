#!/bin/sh

# Migrate DataBase
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('ADMIN_USERNAME')
email = 'user@example.local'
password = os.environ.get('ADMIN_PASSWORD')

if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists or username not provided')
EOF

# Execute server
exec python manage.py runserver 0.0.0.0:8000