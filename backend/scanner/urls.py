from django.urls import path
from .views import scan_text, scan_csv, list_scans, scan_findings, dashboard_stats

urlpatterns = [
    path("scan-text/", scan_text),
    path("scan-csv/", scan_csv),
    path("scans/", list_scans),
    path("scans/<int:scan_id>/findings/", scan_findings),
    path("dashboard-stats/", dashboard_stats),
]