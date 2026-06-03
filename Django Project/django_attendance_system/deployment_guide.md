# Deployment Guide

## Environment Variables

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`

## Production Steps

1. Install dependencies
2. Run migrations
3. Create a superuser
4. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
5. Use PostgreSQL with `DATABASE_URL`
6. Set up a WSGI server such as Gunicorn
7. Place the app behind Nginx or your hosting platform's static file handling

## Recommended Production Settings

- `DEBUG=False`
- Strong `SECRET_KEY`
- `SECURE_SSL_REDIRECT=True` behind HTTPS
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
