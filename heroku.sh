cd server
python manage.py migrate
python manage.py collectstatic
gunicorn settings.wsgi