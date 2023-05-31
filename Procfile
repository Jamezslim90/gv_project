release: python manage.py migrate
web: daphne gv_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A gv_project.celery worker -l info
celerybeat: celery -A gv_project beat -l INFO 