import re
from django.utils import timezone
from .models import Scan, Finding, PIIType


def mask_value(value):
    """
    Simple masking: keep first 2 and last 2 characters.
    """
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def determine_risk(pii_name):
    """
    Basic risk classification logic.
    """
    high_risk = ["ID_NUMBER", "CREDIT_CARD"]
    medium_risk = ["EMAIL", "PHONE"]

    if pii_name in high_risk:
        return "HIGH"
    if pii_name in medium_risk:
        return "MEDIUM"
    return "LOW"


def run_text_scan(data_source, text):
    """
    Runs a synchronous text scan.
    """

    scan = Scan.objects.create(
        data_source=data_source,
        status="RUNNING",
        started_at=timezone.now()
    )

    pii_types = PIIType.objects.all()
    total_findings = 0

    for pii in pii_types:
        pattern = re.compile(pii.regex_pattern)
        matches = pattern.findall(text)

        for match in matches:
            masked = mask_value(match)
            risk = determine_risk(pii.name)

            Finding.objects.create(
                scan=scan,
                pii_type=pii,
                location="TEXT_INPUT",
                masked_value=masked,
                risk_level=risk,
                confidence_score=1.0
            )

            total_findings += 1

    scan.status = "COMPLETED"
    scan.completed_at = timezone.now()
    scan.total_findings = total_findings
    scan.save()

    return scan

import csv
import io


def run_csv_scan(data_source, file):
    """
    Runs a synchronous CSV scan.
    """

    scan = Scan.objects.create(
        data_source=data_source,
        status="RUNNING",
        started_at=timezone.now()
    )

    pii_types = PIIType.objects.all()
    total_findings = 0

    # Read CSV file
    decoded_file = file.read().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(decoded_file))

    for row_number, row in enumerate(csv_reader):

        for column in row:
            text = str(column)

            for pii in pii_types:
                pattern = re.compile(pii.regex_pattern)
                matches = pattern.findall(text)

                for match in matches:
                    masked = mask_value(match)
                    risk = determine_risk(pii.name)

                    Finding.objects.create(
                        scan=scan,
                        pii_type=pii,
                        location=f"ROW_{row_number}",
                        masked_value=masked,
                        risk_level=risk,
                        confidence_score=1.0
                    )

                    total_findings += 1

    scan.status = "COMPLETED"
    scan.completed_at = timezone.now()
    scan.total_findings = total_findings
    scan.save()

    return scan