web: python manage.py collectstatic --noinput;
web: gunicorn gallery.wsgi --log-file - --timeout 120
