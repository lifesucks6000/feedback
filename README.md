# Feedback Portal

A modern feedback management system built with Django and Tailwind CSS.

## Features

- Submit feedback with name and message
- View all feedback submissions
- Edit and delete feedback
- Responsive design
- Modern UI with Tailwind CSS

## Local Development

1. Clone the repository
```bash
git clone <your-repo-url>
cd feedback-portal
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Run the development server
```bash
python manage.py runserver
```

## Deployment to Vercel

1. Fork this repository

2. Create a new project on Vercel

3. Connect your forked repository

4. Configure the following build settings:
   - Framework Preset: Other
   - Build Command: `sh build_files.sh`
   - Output Directory: staticfiles

5. Add the following environment variables:
   - `DJANGO_SECRET_KEY`: Your secret key
   - `DEBUG`: False

6. Deploy!
