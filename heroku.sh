rm ./db.sqlite3
python manage.py migrate
python manage.py collectstatic

export DJANGO_SETTINGS_MODULE=settings.settings_dev
export DJANGO_DB_NAME=default
export DJANGO_SU_NAME=admin
export DJANGO_SU_EMAIL=admin@my.company
export DJANGO_SU_PASSWORD=mypass

python -c "import django; django.setup(); \
   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
   username='$DJANGO_SU_NAME', \
   email='$DJANGO_SU_EMAIL', \
   password='$DJANGO_SU_PASSWORD')"

ls -la
gunicorn settings.wsgi