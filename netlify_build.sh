#!/bin/bash

echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setting up database..."
mkdir -p /tmp
touch /tmp/db.sqlite3
python manage.py migrate --noinput

echo "Creating Netlify _redirects file..."
echo "/*    /index.html   200" > staticfiles/_redirects

echo "Build completed successfully!"
