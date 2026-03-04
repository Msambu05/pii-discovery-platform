from django.db import models

# Represents a system being scanned.
class DataSource(models.Model):
    SOURCE_TYPES = [
        ('DATABASE', 'Database'),
        ('FILE_SYSTEM', 'File System'),
        ('API', 'API'),
        ('MANUAL_UPLOAD', 'Manual Upload'),
    ]

    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    connection_details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# Represents a single execution of a scan.   
class Scan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="scans")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    total_findings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan {self.id} - {self.status}"

# Instead of hardcoding types, we normalize them.
class PIIType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    regex_pattern = models.TextField()  # For detection engine
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#Represents a discovered PII instance.
class Finding(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name="findings")
    pii_type = models.ForeignKey(PIIType, on_delete=models.CASCADE)

    location = models.CharField(max_length=255)  # table/column/file reference
    masked_value = models.CharField(max_length=255)

    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    confidence_score = models.FloatField(default=1.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pii_type.name} - {self.risk_level}"