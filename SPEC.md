# PII Discovery Platform - Technical Specifications

## Document Information

| Property | Value |
|----------|-------|
| **Project Name** | PII Discovery Platform |
| **Version** | 1.0.0 |
| **Document Type** | Technical Specification |
| **Last Updated** | 2025 |

---

## 1. Executive Summary

### 1.1 Purpose

The PII Discovery Platform is a web application designed to scan various data sources (databases, file systems, APIs, and manual uploads) to discover and identify Personally Identifiable Information (PII). It provides a comprehensive solution for data governance and privacy compliance.

### 1.2 Scope

The platform enables organizations to:
- Scan text input for PII detection
- Upload and scan CSV files for PII discovery
- View comprehensive scan statistics and risk distribution
- Track scan history with detailed findings
- Manage multiple data sources for scanning

---

## 2. Technology Stack

### 2.1 Backend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Django | 5.2.11 |
| API | Django REST Framework | 3.16.1 |
| Database | SQLite3 | Built-in |
| CORS | django-cors-headers | 4.9.0 |
| Task Queue | Celery | 5.6.2 |
| Message Broker | Redis | 7.2.1 |

### 2.2 Frontend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | React | 19.2.0 |
| Build Tool | Vite | 7.3.1 |
| HTTP Client | Axios | 1.13.6 |
| Charts | Recharts | 3.7.0 |
| Language | JavaScript/JSX | ES6+ |
| Linter | ESLint | 9.39.1 |

---

## 3. Architecture

### 3.1 System Architecture

```
┌─────────────────┐      ┌─────────────────┐
│    Frontend     │      │     Backend     │
│   (React +      │◄────►│    (Django      │
│    Vite)        │      │   REST API)     │
└─────────────────┘      └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │    SQLite DB    │
                         └─────────────────┘
```

### 3.2 Project Structure

```
pii-discovery-platform/
├── backend/
│   ├── core/
│   │   ├── settings.py      # Django configuration
│   │   ├── urls.py          # URL routing
│   │   ├── asgi.py          # ASGI config
│   │   └── wsgi.py          # WSGI config
│   ├── scanner/
│   │   ├── models.py        # Data models
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # DRF serializers
│   │   ├── services.py      # Business logic
│   │   └── urls.py          # App URL routing
│   ├── db.sqlite3           # SQLite database
│   ├── manage.py            # Django management
│   └── requirements.txt     # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── App.jsx          # Main React component
    │   ├── App.css          # Component styles
    │   ├── main.jsx         # Entry point
    │   └── index.css        # Global styles
    ├── index.html           # HTML template
    ├── package.json         # Node dependencies
    └── vite.config.js       # Vite configuration
```

---

## 4. Data Models

### 4.1 DataSource

Represents a system being scanned for PII.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | Primary Key | Unique identifier |
| name | CharField | max_length=255 | Name of the data source |
| source_type | CharField | max_length=20 | Type: DATABASE, FILE_SYSTEM, API, MANUAL_UPLOAD |
| connection_details | JSONField | nullable, blank | Connection configuration |
| created_at | DateTimeField | auto_now_add | Creation timestamp |

**Source Types:**
- `DATABASE` - Database connection (planned)
- `FILE_SYSTEM` - File system scanning (planned)
- `API` - API endpoint scanning (planned)
- `MANUAL_UPLOAD` - Manual text/CSV input

### 4.2 Scan

Represents a single execution of a scan on a data source.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | Primary Key | Unique identifier |
| data_source | ForeignKey | on_delete=CASCADE | Reference to DataSource |
| status | CharField | max_length=20 | PENDING, RUNNING, COMPLETED, FAILED |
| started_at | DateTimeField | nullable, blank | When scan started |
| completed_at | DateTimeField | nullable, blank | When scan completed |
| total_findings | IntegerField | default=0 | Number of findings discovered |
| created_at | DateTimeField | auto_now_add | Creation timestamp |

**Status Values:**
- `PENDING` - Scan queued but not started
- `RUNNING` - Scan in progress
- `COMPLETED` - Scan finished successfully
- `FAILED` - Scan encountered an error

### 4.3 PIIType

Defines types of PII that can be detected.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | Primary Key | Unique identifier |
| name | CharField | max_length=100 | Name of PII type (e.g., SSN, Email) |
| description | TextField | blank | Description of the PII type |
| regex_pattern | TextField | required | Regex pattern for detection |
| created_at | DateTimeField | auto_now_add | Creation timestamp |

### 4.4 Finding

Represents a discovered PII instance.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | AutoField | Primary Key | Unique identifier |
| scan | ForeignKey | on_delete=CASCADE | Reference to Scan |
| pii_type | ForeignKey | on_delete=CASCADE | Reference to PIIType |
| location | CharField | max_length=255 | Table/column/file reference |
| masked_value | CharField | max_length=255 | Masked version of discovered PII |
| risk_level | CharField | max_length=10 | LOW, MEDIUM, HIGH |
| confidence_score | FloatField | default=1.0 | Detection confidence (0.0-1.0) |
| created_at | DateTimeField | auto_now_add | Creation timestamp |

**Risk Levels:**
- `HIGH` - Critical PII (ID_NUMBER, CREDIT_CARD)
- `MEDIUM` - Sensitive PII (EMAIL, PHONE)
- `LOW` - Low-risk PII (other)

---

## 5. API Endpoints

### 5.1 Scan Operations

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/scan-text/` | Scan text input for PII | `{"text": "string"}` | `{"scan_id": int, "status": string, "total_findings": int}` |
| POST | `/api/scan-csv/` | Upload and scan CSV file | `multipart/form-data` | `{"scan_id": int, "status": string, "total_findings": int}` |
| GET | `/api/scans/` | List all scans | - | Array of Scan objects |
| GET | `/api/scans/<id>/findings/` | Get findings for a scan | - | Array of Finding objects |

### 5.2 Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard-stats/` | Get dashboard statistics |

**Dashboard Response Structure:**
```json
{
  "total_scans": int,
  "total_findings": int,
  "risk_distribution": {
    "high": int,
    "medium": int,
    "low": int
  },
  "findings_by_type": [
    {"pii_type__name": string, "count": int}
  ],
  "findings_by_source": [
    {"scan__data_source__name": string, "count": int}
  ]
}
```

---

## 6. Business Logic

### 6.1 Text Scanning

**Flow:**
1. Receive text input from client
2. Create or retrieve manual data source
3. Create Scan record with status "RUNNING"
4. Iterate through all PIIType patterns
5. Apply regex matching to text
6. For each match, create Finding with:
   - Masked value (first 2 + last 2 characters visible)
   - Risk level based on PII type
   - Confidence score of 1.0
7. Update Scan with total findings and status "COMPLETED"

### 6.2 CSV Scanning

**Flow:**
1. Receive CSV file upload
2. Create or retrieve CSV data source
3. Create Scan record with status "RUNNING"
4. Read CSV using Python's csv module
5. For each cell in each row:
   - Apply all PIIType regex patterns
   - Create Finding for each match
6. Update Scan with total findings and status "COMPLETED"

### 6.3 Risk Classification

```python
HIGH_RISK = ["ID_NUMBER", "CREDIT_CARD"]
MEDIUM_RISK = ["EMAIL", "PHONE"]
# All other PII types default to LOW
```

### 6.4 Value Masking

```python
def mask_value(value):
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]
```

---

## 7. Frontend Components

### 7.1 Main Application (App.jsx)

**State Management:**
- `stats` - Dashboard statistics
- `scans` - List of all scans
- `selectedScan` - Currently selected scan ID
- `findings` - Findings for selected scan
- `inputText` - Text input for scanning
- `selectedFile` - CSV file for upload
- `loading` - Loading state

**Features:**
1. **Text Scanning Section**
   - Textarea for input
   - "Run Scan" button
   - Triggers POST to `/api/scan-text/`

2. **CSV Upload Section**
   - File input with .csv filter
   - "Upload & Scan CSV" button
   - Triggers POST to `/api/scan-csv/`

3. **Statistics Section**
   - Total scans count
   - Total findings count
   - Pie chart showing risk distribution
   - Uses Recharts library

4. **Scans List**
   - Displays all scans with status
   - "View Findings" button per scan
   - Shows scan ID, status, findings count

5. **Findings Viewer**
   - Displays findings for selected scan
   - Shows PII type, masked value, risk level

---

## 8. Security Considerations

### 8.1 Current Implementation

- CORS configured to allow all origins (`CORS_ALLOW_ALL_ORIGINS = True`) - Development only
- No user authentication implemented
- No rate limiting

### 8.2 Recommended for Production

- Implement JWT or session-based authentication
- Restrict CORS to specific origins
- Add rate limiting for API endpoints
- Implement role-based access control (RBAC)
- Add audit logging
- Use HTTPS for all communications

---

## 9. Configuration

### 9.1 Backend Settings (settings.py)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True  # Development only

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'scanner',
]
```

### 9.2 Frontend API Base

```javascript
const API_BASE = "http://127.0.0.1:8000/api";
```

---

## 10. Future Enhancements

### 10.1 Planned Features

| Feature | Description | Priority |
|---------|-------------|----------|
| Database Scanning | Connect to PostgreSQL/MySQL for scanning | High |
| File System Scanning | Scan directories for PII in files | High |
| API Scanning | Scan API responses for PII | Medium |
| Scheduled Scanning | Periodic scans with Celery | Medium |
| User Authentication | Login/registration system | Medium |
| Detailed Reporting | PDF/CSV export of findings | Medium |
| Data Masking/Removal | Option to mask or delete PII | Low |
| Custom PII Types | UI to add custom PII patterns | Low |

### 10.2 Infrastructure

- Replace SQLite with PostgreSQL for production
- Set up Celery with Redis for background tasks
- Containerize with Docker
- Set up CI/CD pipeline

---

## 11. Testing

### 11.1 Backend Tests

Tests should cover:
- Model creation and validation
- Serializer functionality
- API endpoint responses
- Service layer logic (scanning algorithms)
- CSV parsing

### 11.2 Frontend Tests

Tests should cover:
- Component rendering
- API integration
- State management
- User interactions

---

## 12. Deployment

### 12.1 Backend Deployment

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 12.2 Frontend Deployment

```bash
cd frontend
npm install
npm run dev
```

### 12.3 Production Build

```bash
cd frontend
npm install
npm run build
```

The built files will be in `frontend/dist/` and can be served by Django or any static file server.

---

## 13. Glossary

| Term | Definition |
|------|------------|
| PII | Personally Identifiable Information - Data that can identify an individual |
| Scan | An execution of the PII discovery process |
| Finding | A discovered instance of PII |
| Data Source | A system or location being scanned |
| Risk Level | Classification of PII severity (HIGH/MEDIUM/LOW) |
| Masking | Process of hiding部分 of sensitive data |

---

## 14. References

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- React Documentation: https://react.dev/
- Vite Documentation: https://vitejs.dev/
- Recharts: https://recharts.org/

---

*End of Specification Document*

