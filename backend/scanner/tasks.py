from celery import shared_task
from .services import run_csv_scan, run_text_scan
from .models import DataSource


@shared_task
def run_csv_scan_task(file_path):
    data_source, _ = DataSource.objects.get_or_create(
        name="CSV Upload",
        source_type="FILE"
    )

    with open(file_path, 'rb') as f:
        run_csv_scan(data_source, f)


@shared_task
def run_text_scan_task(text):
    data_source, _ = DataSource.objects.get_or_create(
        name="Manual Text Input",
        source_type="MANUAL_UPLOAD"
    )

    run_text_scan(data_source, text)