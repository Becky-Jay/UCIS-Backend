# UCIS Backend — Django

Django REST Framework backend for the UDSM Campus Information System.

## User Roles
- **student** — Academic access, feed, events, mentorship requests
- **alumni** — Network, career opportunities, mentorship, events
- **college_admin** — Manage college-level users, announcements, events, news
- **system_admin** — Full system access, user management, audit logs, dashboard

## Quick Start

```bash
cd ucis_django

# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and configure environment
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
# Edit .env with your settings

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (system_admin)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver 0.0.0.0:7000
```

## API Endpoints

| Prefix | Description |
|---|---|
| `/api/authentication/` | Register, login, forgot/reset password, logout |
| `/api/users/` | User CRUD, profiles, engagement stats |
| `/api/announcements/` | Announcements (CRUD, role-filtered) |
| `/api/news/` | News articles |
| `/api/events/` | Events + registration |
| `/api/feed/` | Posts, reactions, comments |
| `/api/mentorshipRequest/` | Mentorship requests (student↔alumni) |
| `/api/alumni/` | Alumni profiles, verification |
| `/api/emergencyContacts/` | Emergency contacts |
| `/api/notifications/` | In-app notifications |
| `/api/auditLogs/` | Admin audit trail |
| `/api/dashboard/` | Role-based dashboard stats |
| `/api/token/refresh/` | Refresh JWT access token |

## Authentication

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

Obtain tokens via `POST /api/authentication/login/`.  
Refresh via `POST /api/token/refresh/` with `{"refresh": "<refresh_token>"}`.

## Database

Default: **SQLite** (development).  
For PostgreSQL, update `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ucis_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```
Then `pip install psycopg2-binary` and re-run `python manage.py migrate`.
