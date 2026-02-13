# StayFlow Hotel Management System (Production-Ready MVP)

Full-stack Hotel PMS using Django REST Framework + React (Vite).

## Included Modules
- Authentication + JWT authorization
- Guests, Rooms, Bookings, Service Requests, Invoices, Notifications
- Role model: Admin, Manager, Front Desk, Housekeeping, Accountant, Guest
- Dashboard analytics and health endpoint

## Enterprise Additions Implemented
- Dockerized deployment with PostgreSQL and Nginx reverse proxy
- CI pipeline (GitHub Actions): backend tests + frontend build
- Advanced frontend RBAC: route guards + role-filtered navigation
- Notification provider integration:
  - Email via Django email backend (SMTP supported)
  - SMS via outbound webhook integration
- Security hardening:
  - Production-only secure cookie/HSTS/proxy settings
  - Strict secret key handling in non-debug mode
  - Logging to file + console
- Backup tooling:
  - PostgreSQL dump script
  - SQLite backup script

## API Endpoints
- `POST /api/auth/login/`
- `POST /api/auth/signup/`
- `POST /api/auth/logout/`
- `GET|POST /api/guests/`
- `GET|POST /api/rooms/`
- `GET|POST /api/bookings/`
- `POST /api/bookings/{id}/reschedule/`
- `POST /api/bookings/{id}/cancel/`
- `GET|POST /api/services/`
- `GET /api/services/{id}/versions/`
- `GET|POST /api/invoices/`
- `POST /api/invoices/generate/`
- `POST /api/invoices/{id}/mark_paid/`
- `GET /api/invoices/{id}/invoice_pdf/`
- `GET /api/dashboard/`
- `POST /api/notifications/send_reminder/`
- `GET /api/health/`

## Local Setup
1. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

2. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Docker Setup (Production-style)
```bash
docker compose up --build
```

Services:
- Frontend (Nginx): `http://localhost`
- Backend API via Nginx proxy: `http://localhost/api/`
- Health check: `http://localhost/health`

## CI
GitHub workflow: `.github/workflows/ci.yml`
- Python dependency install + migrations + pytest
- Node dependency install + production build

## Notification Provider Config
Set in `backend/.env`:
- Email: `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
- SMS: `SMS_WEBHOOK_URL`, `SMS_WEBHOOK_TOKEN`

If `SMS_WEBHOOK_URL` is empty, SMS sends will fail with explicit error and be logged as failed.

## Backup Scripts
- PostgreSQL backup: `scripts/backup_postgres.sh`
- SQLite backup (Windows): `scripts/backup_sqlite.ps1`

Examples:
```bash
sh scripts/backup_postgres.sh
```
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\backup_sqlite.ps1
```

## Frontend Assets
- `frontend/src/assets/images/stayflow-logo.svg`
- `frontend/src/assets/images/hotel-hero.svg`
