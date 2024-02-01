#!/bin/bash

APP_PORT=${PORT:-8000}

cd /app/

# Run migrations
/opt/venv/bin/python manage.py migrate

# Create admin user
/opt/venv/bin/python manage.py create_admin_user

# Run gunicorn
/opt/venv/bin/gunicorn assignment.wsgi:application --bind "0.0.0.0:${APP_PORT}"