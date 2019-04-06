cd server
python manage.py migrate
python manage.py collectstatic
ls -la
gunicorn settings.wsgi