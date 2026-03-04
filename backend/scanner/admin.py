from django.contrib import admin
from .models import DataSource, Scan, PIIType, Finding


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "source_type", "created_at")
    search_fields = ("name",)
    list_filter = ("source_type",)


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("id", "data_source", "status", "total_findings", "created_at")
    list_filter = ("status",)
    search_fields = ("data_source__name",)


@admin.register(PIIType)
class PIITypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("id", "pii_type", "risk_level", "scan", "created_at")
    list_filter = ("risk_level", "pii_type")