# Django Student Attendance Management System

A production-ready Django 5+ project for managing student attendance, notices, and reports for schools or colleges.

## Features

- Admin and student roles
- Student management with search and pagination
- Daily attendance marking with duplicate protection
- Notice board with important pinning
- Dashboard analytics for admin and students
- PDF and Excel report export
- Responsive Bootstrap 5 UI
- SQLite development setup with PostgreSQL support for production

## Quick Start

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from `.env.example`.

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Seed sample data:
   ```bash
   python manage.py seed_demo_data
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

## Login Model

- Admin users log in with Django staff/superuser accounts.
- Students log in with Django auth accounts linked to `Student.user`.

## Notes

- Attendance is stored per student per date.
- Historical records are never deleted.
- Attendance for previous dates can be edited by admin.
- "Reset every new day" means a fresh daily attendance entry screen; old records remain intact.

## Production Notes

- Use PostgreSQL in production by setting `DATABASE_URL`.
- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS`.
- Serve static and media files through your web server or a platform-specific solution.

## Default URLs

- `/accounts/login/`
- `/admin-dashboard/`
- `/student-dashboard/`
- `/students/`
- `/attendance/`
- `/notices/`
- `/reports/`
