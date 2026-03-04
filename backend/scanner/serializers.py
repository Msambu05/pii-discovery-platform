from rest_framework import serializers
from .models import Scan, Finding


class FindingSerializer(serializers.ModelSerializer):
    pii_type = serializers.CharField(source="pii_type.name")

    class Meta:
        model = Finding
        fields = [
            "id",
            "pii_type",
            "location",
            "masked_value",
            "risk_level",
            "confidence_score",
            "created_at"
        ]


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = [
            "id",
            "status",
            "total_findings",
            "started_at",
            "completed_at",
            "created_at"
        ]