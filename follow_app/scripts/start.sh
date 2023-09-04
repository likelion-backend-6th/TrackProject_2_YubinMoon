#! /bin/sh

echo start server

python manage.py migrate
python manage.py runserver
