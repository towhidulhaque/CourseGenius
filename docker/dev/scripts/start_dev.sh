#!/usr/bin/env sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate --no-input

# this creates a default superuser if there are no users
# see backend/accounts/management/commands/create_default_user.py
# python manage.py create_default_user
while true; do
    python manage.py runserver 0.0.0.0:8000 --traceback
    sleep 5s
done
