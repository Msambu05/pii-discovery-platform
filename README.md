# PII Discovery Platform

## Project Overview

The PII Discovery Platform is a web application designed to scan various data sources (databases, file systems, APIs) to discover and identify Personally Identifiable Information (PII). It provides a comprehensive solution for data governance and privacy compliance.

## Project Structure

```
pii-discovery-platform/
├── backend/                 # Django REST API backend
│   ├── core/               # Django project settings
│   │   ├── settings.py     # Main configuration
│   │   ├── urls.py         # URL routing
│   │   ├── asgi.py         # ASGI configuration
│   │   └── wsgi.py         # WSGI configuration
│   ├── scanner/            # Scanner app (main functionality)
│   │   ├── models.py       # Data models
│   │   ├── views.py        # API views
│   │   ├── admin.py        # Django admin configuration
│   │   ├── apps.py         # App configuration
│   │   └── migrations/     # Database migrations
│   ├── db.sqlite3          # SQLite database
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
│
└── frontend/               # React + Vite frontend
    ├── src/
    │   ├── App.jsx         # Main React component
    │   ├── App.css         # Styles
    │   ├── main.jsx        # Entry point
    │   └── index.css       # Global styles
    ├── index.html          # HTML template
    ├── package.json        # Node.js dependencies
    └── vite.config.js     # Vite configuration
```

## Technology Stack

### Backend
- **Framework**: Django 5.2.11
- **API**: Django REST Framework 3.16.1
- **Database**: SQLite3
- **CORS**: django-cors-headers 4.9.0
- **Task Queue**: Celery 5.6.2 (configured but not yet integrated)
- **Message Broker**: Redis 7.2.1 (for Celery)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: JavaScript/JSX
- **Linter**: ESLint

## Data Models

### DataSource
Represents a system being scanned for PII.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(255) | Name of the data source |
| source_type | CharField | Type: DATABASE, FILE_SYSTEM, API, MANUAL_UPLOAD |
| connection_details | JSONField | Connection configuration |
| created_at | DateTimeField | Creation timestamp |

### Scan
Represents a single execution of a scan on a data source.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| data_source | ForeignKey | Reference to DataSource |
| status | CharField | PENDING, RUNNING, COMPLETED, FAILED |
| started_at | DateTimeField | When scan started |
| completed_at | DateTimeField | When scan completed |
| total_findings | IntegerField | Number of findings discovered |
| created_at | DateTimeField | Creation timestamp |

### PIIType
Defines types of PII that can be detected.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(100) | Name of PII type (e.g., SSN, Email) |
| description | TextField | Description of the PII type |
| regex_pattern | TextField | Regex pattern for detection |
| created_at | DateTimeField | Creation timestamp |

### Finding
Represents a discovered PII instance.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| scan | ForeignKey | Reference to Scan |
| pii_type | ForeignKey | Reference to PIIType |
| location | CharField(255) | Table/column/file reference |
| masked_value | CharField(255) | Masked version of discovered PII |
| risk_level | CharField | LOW, MEDIUM, HIGH |
| confidence_score | FloatField | Detection confidence (0.0-1.0) |
| created_at | DateTimeField | Creation timestamp |

## Current Status

### Implemented
1. ✅ Django project setup with REST Framework
2. ✅ Scanner app with all data models (DataSource, Scan, PIIType, Finding)
3. ✅ Database migrations
4. ✅ CORS configuration for frontend-backend communication
5. ✅ Basic React + Vite frontend setup
6. ✅ Celery and Redis configuration (ready for async task processing)

### Pending Implementation
1. ❌ API views and endpoints for scanner operations
2. ❌ URL routing for API endpoints
3. ❌ Frontend UI components for:
   - Data source management
   - Scan execution and monitoring
   - Finding visualization and reporting
4. ❌ PII detection engine (regex-based scanning)
5. ❌ Celery task integration for background scanning

## Getting Started

### Backend Setup

```
bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Frontend Setup

```
bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Configuration

### CORS Settings
The backend is configured to allow all origins for development:
```
python
CORS_ALLOW_ALL_ORIGINS = True
```

### Database
Currently using SQLite (`db.sqlite3`). For production, update `DATABASES` in `settings.py` to use PostgreSQL or another database.

## Future Enhancements

1. **PII Detection Engine**: Implement regex-based scanning for various PII types
2. **Multiple Data Source Support**: Add support for more data source types
3. **Scan Scheduling**: Implement periodic scanning with Celery
4. **Reporting**: Generate detailed reports on discovered PII
5. **Data Masking**: Provide data masking/removal capabilities
6. **User Authentication**: Add user authentication and authorization

## License

This project is for demonstration purposes.
