#!/bin/bash

# Django Heroku Deployment Helper Script

echo "🚀 Django Heroku Deployment Helper"
echo "================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   brew tap heroku/brew && brew install heroku"
    exit 1
fi

echo "✅ Heroku CLI is installed"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Initializing..."
    git init
    git add .
    git commit -m "Initial commit"
fi

echo "✅ Git repository ready"

# Login to Heroku (if not already logged in)
echo "🔐 Checking Heroku authentication..."
heroku whoami &> /dev/null || {
    echo "Please log in to Heroku:"
    heroku login
}

echo "✅ Heroku authentication successful"

# Prompt for app name
read -p "Enter your Heroku app name (or press Enter for auto-generated): " app_name

# Create Heroku app
if [ -z "$app_name" ]; then
    echo "📱 Creating Heroku app with auto-generated name..."
    heroku create
else
    echo "📱 Creating Heroku app: $app_name"
    heroku create $app_name
fi

# Get the app URL
app_url=$(heroku info -s | grep web_url | cut -d= -f2)
echo "🌐 Your app URL will be: $app_url"

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set DEBUG=False
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True
heroku config:set SECURE_HSTS_SECONDS=31536000
heroku config:set SECURE_HSTS_INCLUDE_SUBDOMAINS=True
heroku config:set SECURE_HSTS_PRELOAD=True

# Generate a new secret key
secret_key=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set DJANGO_SECRET_KEY="$secret_key"

# Add PostgreSQL addon
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini

echo "📝 Please update your CSRF_TRUSTED_ORIGINS in settings.py to include: $app_url"
echo "💡 You can do this by running:"
echo "   Add '$app_url' to the CSRF_TRUSTED_ORIGINS list in config/settings.py"

echo ""
echo "🚀 Ready to deploy! Run the following commands:"
echo "   git add ."
echo "   git commit -m 'Prepare for Heroku deployment'"
echo "   git push heroku main"
echo "   heroku run python manage.py migrate"
echo "   heroku run python manage.py createsuperuser"
echo ""
echo "🎉 Your app will be available at: $app_url"
