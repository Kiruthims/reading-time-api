#!/usr/bin/env bash
# Exit script on any error
set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect all static files into the 'staticfiles' directory
python manage.py collectstatic --noinput

# Apply any database migrations
python manage.py migrate