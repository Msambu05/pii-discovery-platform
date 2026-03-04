from django.urls import path
from .views import scan_text, list_scans, scan_findings, dashboard_stats

urlpatterns = [
    path("scan-text/", scan_text),
    path("scans/", list_scans),
    path("scans/<int:scan_id>/findings/", scan_findings),
    path("dashboard-stats/", dashboard_stats),
]