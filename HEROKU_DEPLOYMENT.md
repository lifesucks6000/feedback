# Django Heroku Deployment Guide (Web Dashboard)

This guide will help you deploy your Django feedback application to Heroku using the **Heroku Web Dashboard** (GUI method).

## Prerequisites

1. **Heroku Account**: Sign up at [https://signup.heroku.com](https://signup.heroku.com) if you don't have one
2. **GitHub Account**: Your code should be pushed to a GitHub repository
3. **Git**: Ensure your project is in a Git repository and pushed to GitHub

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

## Files Added for Heroku Deployment

Your project is already configured with the necessary files for Heroku deployment:

### 1. Procfile
```
web: gunicorn config.wsgi --log-file -
```
This tells Heroku how to run your Django application using Gunicorn.

### 2. runtime.txt
```
python-3.11.5
```
Specifies the Python version for Heroku to use.

### 3. Updated requirements.txt
The following packages have been added for production deployment:
- `gunicorn`: WSGI HTTP server for Python
- `dj-database-url`: Simplified database configuration
- `psycopg2-binary`: PostgreSQL adapter for Python

### 4. Production-Ready settings.py
Your Django settings are configured to:
- Use environment variables for security settings
- Automatically switch from SQLite (development) to PostgreSQL (production)
- Handle static files with WhiteNoise

---

## Step-by-Step GUI Deployment

### Step 1: Prepare Your GitHub Repository

**Before starting, ensure your code is on GitHub:**

```bash
# If not already done, push your code to GitHub
git add .
git commit -m "Prepare for Heroku deployment"
git push origin main
```

### Step 2: Access Heroku Dashboard

1. Go to **[https://dashboard.heroku.com](https://dashboard.heroku.com)**
2. **Login** with your Heroku account credentials
3. You'll see your Heroku dashboard with any existing apps

### Step 3: Create a New App

1. Click the **"New"** button (top-right corner)
2. Select **"Create new app"**
3. **App Settings:**
   - **App name**: Choose a unique name (e.g., `my-feedback-app-2025`)
   - **Region**: Choose "United States" or "Europe"
4. Click **"Create app"**

🎉 **Your app is created!** Note your app URL: `https://your-app-name.herokuapp.com`

### Step 4: Connect to GitHub Repository

1. In your app dashboard, click the **"Deploy"** tab
2. In the **"Deployment method"** section:
   - Click **"GitHub"**
   - Click **"Connect to GitHub"**
   - **Authorize Heroku** to access your GitHub account (if prompted)
3. **Search for your repository:**
   - Type your repository name in the search box
   - Click **"Search"**
   - Find your repository and click **"Connect"**

✅ **Repository connected successfully!**

### Step 5: Configure Environment Variables

1. Click the **"Settings"** tab
2. Scroll down to **"Config Vars"** section
3. Click **"Reveal Config Vars"**
4. **Add the following environment variables** (click "Add" for each):

| KEY | VALUE | Purpose |
|-----|-------|---------|
| `DEBUG` | `False` | Disable debug mode in production |
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS redirects |
| `SESSION_COOKIE_SECURE` | `True` | Secure session cookies over HTTPS |
| `CSRF_COOKIE_SECURE` | `True` | Secure CSRF cookies over HTTPS |
| `SECURE_HSTS_SECONDS` | `31536000` | HTTP Strict Transport Security (1 year) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `True` | Include subdomains in HSTS |
| `SECURE_HSTS_PRELOAD` | `True` | Enable HSTS preload |
| `DJANGO_SECRET_KEY` | `your-secret-key-here` | **See below for generation** |

**🔐 To generate a Django secret key:**
- **Option 1**: Run in your local terminal: 
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- **Option 2**: Use an online Django secret key generator
- **Copy the generated key** and paste it as the value for `DJANGO_SECRET_KEY`

### Step 6: Add PostgreSQL Database

1. Still in the **"Settings"** tab, scroll to **"Add-ons"** section
2. Click **"Find more add-ons"** or search for **"postgres"**
3. Find **"Heroku Postgres"** and click it
4. **Select a plan:**
   - **Mini ($5/month)**: Good for small apps
   - **Basic ($9/month)**: Better performance
5. Click **"Submit Order Form"**

✅ **Database added!** This automatically creates a `DATABASE_URL` config variable.

### Step 7: Update CSRF Settings

**Important**: You need to add your Heroku app URL to your Django settings.

1. **Open your `config/settings.py` file** in your code editor
2. **Find the `CSRF_TRUSTED_ORIGINS` section** (around line 131)
3. **Add your Heroku app URL:**

```python
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000', 
    'http://127.0.0.1:8000',
    'https://your-actual-app-name.herokuapp.com',  # Add this line
]
```

4. **Replace `your-actual-app-name`** with your real Heroku app name
5. **Save the file** and **commit the changes:**

```bash
git add config/settings.py
git commit -m "Add Heroku URL to CSRF_TRUSTED_ORIGINS"
git push origin main
```

### Step 8: Deploy Your Application

1. Go back to the **"Deploy"** tab in Heroku dashboard
2. Scroll to **"Manual deploy"** section
3. **Select branch**: Choose `main` (or your default branch)
4. Click **"Deploy Branch"**

🚀 **Deployment in progress!** You'll see real-time build logs:
- Installing dependencies
- Collecting static files
- Building your app

⏱️ **Wait for completion** (usually 2-5 minutes)

### Step 9: Run Database Migrations

After successful deployment:

1. Click **"More"** menu (top-right corner of your app dashboard)
2. Select **"Run console"**
3. **Type**: `python manage.py migrate`
4. Click **"Run"**

✅ **Database migrations completed!**

### Step 10: Create Admin User (Optional)

To access Django admin:

1. Again, click **"More"** → **"Run console"**
2. **Type**: `python manage.py createsuperuser`
3. **Follow the prompts** to create username, email, and password
4. Click **"Run"**

### Step 11: Open Your Live App! 🎉

1. Click the **"Open app"** button (top-right corner)
2. **Your Django feedback app is now live!**

---

## Enable Automatic Deployments (Recommended)

**Set up automatic deployments** so your app updates whenever you push to GitHub:

1. In the **"Deploy"** tab, scroll to **"Automatic deploys"**
2. **Select branch**: Choose `main`
3. ☑️ **Check**: "Wait for CI to pass before deploy" (if you have CI/CD)
4. Click **"Enable Automatic Deploys"**

🔄 **Now every GitHub push will automatically deploy to Heroku!**

---

## Post-Deployment Management

### View Application Logs
1. Go to **"More"** → **"View logs"**
2. Monitor real-time application logs
3. **Useful for debugging** any issues

### Restart Your Application
1. Go to **"More"** → **"Restart all dynos"**
2. Restarts your application (helpful if it's stuck)

### Scale Your Application
1. Go to **"Resources"** tab
2. **Edit the "web" dyno**
3. **Adjust the slider** to scale up/down
4. Click **"Confirm"**

### Manage Database
1. **Resources** tab → Click **"Heroku Postgres"**
2. View database statistics
3. Access database credentials
4. **Reset database** (⚠️ **Warning**: Deletes all data)

---

## Troubleshooting Common Issues

### 🚨 Build Fails
- **Check build logs** in the Deploy tab
- **Verify** `requirements.txt` has all dependencies
- **Ensure** Python version in `runtime.txt` is supported

### 🚨 App Crashes
- **View logs**: More → View logs
- **Common causes**:
  - Missing environment variables
  - Database migration issues
  - Static file problems

### 🚨 Static Files Not Loading
- **Check** that `STATIC_ROOT` and `STATICFILES_DIRS` are configured
- **WhiteNoise** is already configured in your settings

### 🚨 Database Errors
- **Ensure migrations are run**: More → Run console → `python manage.py migrate`
- **Check** that PostgreSQL add-on is installed

### 🚨 CSRF Token Errors
- **Verify** your Heroku app URL is in `CSRF_TRUSTED_ORIGINS`
- **Redeploy** after updating settings

---

## Next Steps & Best Practices

### 🔧 Recommended Improvements

1. **Custom Domain**: 
   - Settings tab → Domains and certificates
   - Add your custom domain

2. **SSL Certificate**:
   - Heroku provides free SSL
   - Configure in Settings → SSL Certificates

3. **Monitoring**:
   - Add Heroku add-ons for monitoring
   - Set up error tracking (e.g., Sentry)

4. **Environment Management**:
   - Create staging environment
   - Use review apps for PR testing

5. **Backup Strategy**:
   - Set up database backups
   - Use Heroku Postgres backup features

### 📚 Useful Dashboard Features

- **Activity Feed**: Track all deployments and changes
- **Metrics**: Monitor app performance
- **Collaborators**: Add team members
- **Webhooks**: Integrate with external services

---

## Your App is Live! 🎉

Your Django feedback application is now successfully deployed on Heroku!

**App URL**: `https://your-app-name.herokuapp.com`
**Admin URL**: `https://your-app-name.herokuapp.com/admin`

### Quick Commands Summary

| Task | GUI Location |
|------|-------------|
| **Deploy** | Deploy tab → Manual deploy |
| **View Logs** | More → View logs |
| **Run Commands** | More → Run console |
| **Environment Variables** | Settings → Config Vars |
| **Add Database** | Settings → Add-ons |
| **Scale App** | Resources → Edit dynos |
| **Custom Domain** | Settings → Domains |

**Happy deploying! 🚀**
