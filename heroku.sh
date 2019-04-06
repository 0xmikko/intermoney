cd server
python manage.py migrate
gunicorn settings.wsgi