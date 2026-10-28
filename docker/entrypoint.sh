#!/bin/sh
set -e

echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static assets..."
python manage.py collectstatic --noinput

echo "Initiating default car data..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()
from djangoapp.populate import initiate
initiate()
" || true

exec "$@"
