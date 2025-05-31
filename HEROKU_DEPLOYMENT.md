# Django Heroku Deployment Guide

This guide will help you deploy your Django feedback application to Heroku.

## Prerequisites

1. **Heroku CLI**: Install the Heroku CLI
   ```bash
   # On macOS
   brew tap heroku/brew && brew install heroku
   
   # On Ubuntu/Debian
   sudo snap install --classic heroku
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Git**: Ensure your project is in a Git repository
3. **Heroku Account**: Sign up at https://heroku.com

## Files Added for Heroku Deployment

### 1. Procfile
```
web: gunicorn config.wsgi --log-file -
```
This tells Heroku how to run your application.

### 2. runtime.txt
```
python-3.11.5
```
Specifies the Python version for Heroku.

### 3. Updated requirements.txt
Added the following packages:
- `gunicorn`: WSGI HTTP server for Python
- `dj-database-url`: Simplified database configuration
- `psycopg2-binary`: PostgreSQL adapter for Python

## Manual Deployment Steps

### Step 1: Login to Heroku
```bash
heroku login
```

### Step 2: Create a Heroku App
```bash
# Option 1: Auto-generated name
heroku create

# Option 2: Custom name
heroku create your-app-name
```

### Step 3: Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set SESSION_COOKIE_SECURE=True
heroku config:set CSRF_COOKIE_SECURE=True
heroku config:set SECURE_HSTS_SECONDS=31536000
heroku config:set SECURE_HSTS_INCLUDE_SUBDOMAINS=True
heroku config:set SECURE_HSTS_PRELOAD=True

# Generate and set a secret key
heroku config:set DJANGO_SECRET_KEY="your-secret-key-here"
```

### Step 4: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Update CSRF_TRUSTED_ORIGINS
Add your Heroku app URL to the `CSRF_TRUSTED_ORIGINS` list in `config/settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000', 
    'http://127.0.0.1:8000',
    'https://your-app-name.herokuapp.com',  # Add this line
]
```

### Step 6: Deploy to Heroku
```bash
# Add all files to git
git add .

# Commit changes
git commit -m "Prepare for Heroku deployment"

# Push to Heroku
git push heroku main
```

### Step 7: Run Database Migrations
```bash
heroku run python manage.py migrate
```

### Step 8: Create a Superuser (Optional)
```bash
heroku run python manage.py createsuperuser
```

### Step 9: Open Your App
```bash
heroku open
```

## Automated Deployment (Using the Script)

We've created a deployment script that automates most of these steps:

```bash
./deploy_heroku.sh
```

This script will:
- Check if Heroku CLI is installed
- Initialize git repository if needed
- Log you into Heroku
- Create a Heroku app
- Set environment variables
- Add PostgreSQL database
- Provide next steps

## Post-Deployment

### Collect Static Files (if needed)
```bash
heroku run python manage.py collectstatic --noinput
```

### View Logs
```bash
heroku logs --tail
```

### Scale Your App
```bash
heroku ps:scale web=1
```

## Environment Variables Configured

The following environment variables are set for production:

- `DEBUG=False`: Disables debug mode in production
- `SECURE_SSL_REDIRECT=True`: Forces HTTPS redirects
- `SESSION_COOKIE_SECURE=True`: Secure session cookies
- `CSRF_COOKIE_SECURE=True`: Secure CSRF cookies
- `SECURE_HSTS_SECONDS=31536000`: HTTP Strict Transport Security
- `DJANGO_SECRET_KEY`: Production secret key

## Database Configuration

Your Django app is configured to:
- Use SQLite for local development
- Automatically switch to PostgreSQL when deployed to Heroku (using the `DATABASE_URL` environment variable)

## Troubleshooting

### Common Issues:

1. **Build fails**: Check your `requirements.txt` for version conflicts
2. **App crashes**: Check logs with `heroku logs --tail`
3. **Static files not loading**: Run `heroku run python manage.py collectstatic`
4. **Database errors**: Ensure migrations are run with `heroku run python manage.py migrate`

### Useful Commands:

```bash
# Check app status
heroku ps

# View configuration
heroku config

# Access Django shell on Heroku
heroku run python manage.py shell

# View database info
heroku pg:info

# Reset database (WARNING: This deletes all data)
heroku pg:reset DATABASE_URL
```

## Next Steps

1. Set up continuous deployment from GitHub
2. Configure custom domain name
3. Add monitoring and logging
4. Set up staging environment
5. Configure email backend for production

Your Django feedback app should now be live on Heroku! 🎉
