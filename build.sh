#!/bin/bash

# Install python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create database directory
mkdir -p /tmp
touch /tmp/db.sqlite3
python manage.py migrate --noinput
