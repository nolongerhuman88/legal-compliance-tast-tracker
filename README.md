# Legal Compliance Task Tracker

Aplikasi web untuk memantau tugas kepatuhan legal dengan autentikasi role-based, dashboard analitik, reminder H-7, dan audit log perubahan task.

## Tech Stack
- Backend: Flask
- ORM: SQLAlchemy
- DB: PostgreSQL
- Frontend: HTML + Bootstrap 5
- Migration: Flask-Migrate (Alembic)
- Testing: pytest

## Struktur Folder
```
legal-compliance-tast-tracker/
├── app/
│   ├── controllers/
│   ├── models/
│   ├── services/
│   ├── templates/
│   ├── config.py
│   ├── extensions.py
│   ├── forms.py
│   └── __init__.py
├── migrations/
│   └── versions/
├── tests/
├── .env.example
├── requirements.txt
├── run.py
└── seed.py
```

## Setup
1. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy environment file:
   ```bash
   cp .env.example .env
   ```
3. Jalankan migration:
   ```bash
   flask --app run.py db upgrade
   ```
4. Seed data contoh:
   ```bash
   python seed.py
   ```
5. Jalankan aplikasi:
   ```bash
   python run.py
   ```

## Akun Seed
- admin / Admin123!
- officer / Officer123!
- reviewer / Reviewer123!

## Testing
```bash
pytest
```
