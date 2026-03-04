from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .serializers import ScanSerializer, FindingSerializer
from .models import Scan, Finding
from .models import DataSource
from .services import run_text_scan


@api_view(["POST"])
def scan_text(request):
    text = request.data.get("text")

    if not text:
        return Response({"error": "No text provided"}, status=400)

    # For now create or get a default data source
    data_source, _ = DataSource.objects.get_or_create(
        name="Manual Text Input",
        source_type="MANUAL_UPLOAD"
    )

    scan = run_text_scan(data_source, text)

    return Response({
        "scan_id": scan.id,
        "status": scan.status,
        "total_findings": scan.total_findings
    })

@api_view(["GET"])
def list_scans(request):
    scans = Scan.objects.all().order_by("-created_at")
    serializer = ScanSerializer(scans, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def scan_findings(request, scan_id):
    findings = Finding.objects.filter(scan_id=scan_id)
    serializer = FindingSerializer(findings, many=True)
    return Response(serializer.data)

# Dashboard stats endpoint
@api_view(["GET"])
def dashboard_stats(request):
    total_scans = Scan.objects.count()
    total_findings = Finding.objects.count()

    high_risk = Finding.objects.filter(risk_level="HIGH").count()
    medium_risk = Finding.objects.filter(risk_level="MEDIUM").count()
    low_risk = Finding.objects.filter(risk_level="LOW").count()

    findings_by_type = (
        Finding.objects
        .values("pii_type__name")
        .annotate(count=Count("id"))
    )

    findings_by_source = (
        Finding.objects
        .values("scan__data_source__name")
        .annotate(count=Count("id"))
    )

    return Response({
        "total_scans": total_scans,
        "total_findings": total_findings,
        "risk_distribution": {
            "high": high_risk,
            "medium": medium_risk,
            "low": low_risk,
        },
        "findings_by_type": findings_by_type,
        "findings_by_source": findings_by_source,
    })