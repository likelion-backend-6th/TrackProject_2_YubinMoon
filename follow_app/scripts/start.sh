#! /bin/sh

echo start server

python manage.py collectstatic
python manage.py migrate
gunicorn config.wsgi:application --config config/gunicorn_config.py
