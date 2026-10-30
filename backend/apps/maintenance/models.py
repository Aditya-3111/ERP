from django.db import models
from apps.core.models import User
from apps.inventory.models import StockItem
import uuid


class AssetCategory(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=200)
    category_code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    depreciation_method = models.CharField(max_length=10, default='SLM')
    useful_life_years = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'mnt_asset_categories'

    def __str__(self):
        return self.category_name


class Asset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'), ('inactive', 'Inactive'), ('under_maintenance', 'Under Maintenance'),
        ('scrapped', 'Scrapped'), ('sold', 'Sold'), ('idle', 'Idle')
    ]
    CRITICALITY_CHOICES = [
        ('critical', 'Critical'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_code = models.CharField(max_length=50, unique=True)
    asset_name = models.CharField(max_length=200)
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True)
    asset_type = models.CharField(max_length=20, default='machine')
    model_no = models.CharField(max_length=100, blank=True)
    serial_no = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    supplier = models.CharField(max_length=200, blank=True)
    purchase_date = models.DateField(null=True)
    purchase_price = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    warranty_start = models.DateField(null=True)
    warranty_end = models.DateField(null=True)
    current_value = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    location = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    responsible_person = models.CharField(max_length=100, blank=True)
    criticality = models.CharField(max_length=10, default='medium', choices=CRITICALITY_CHOICES)
    status = models.CharField(max_length=30, default='active', choices=STATUS_CHOICES)
    barcode = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='assets/', blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mnt_assets'

    def __str__(self):
        return f"{self.asset_code} - {self.asset_name}"


class MaintenanceSchedule(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'), ('weekly', 'Weekly'), ('biweekly', 'Biweekly'),
        ('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'), ('yearly', 'Yearly'),
        ('meter_based', 'Meter Based'), ('custom', 'Custom')
    ]
    STATUS_CHOICES = [('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_name = models.CharField(max_length=200)
    schedule_code = models.CharField(max_length=50, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    frequency_type = models.CharField(max_length=20, default='monthly', choices=FREQUENCY_CHOICES)
    frequency_value = models.IntegerField(default=1)
    last_performed_date = models.DateField(null=True)
    next_due_date = models.DateField(null=True)
    estimated_duration_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    estimated_cost = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    assigned_technician = models.CharField(max_length=100, blank=True)
    priority = models.CharField(max_length=10, default='medium')
    status = models.CharField(max_length=20, default='active', choices=STATUS_CHOICES)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'mnt_schedules'

    def __str__(self):
        return self.schedule_name


class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('closed', 'Closed')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
        ('critical', 'Critical'), ('emergency', 'Emergency')
    ]

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wo_no = models.CharField(max_length=100, unique=True)
    wo_date = models.DateField()
    wo_type = models.CharField(max_length=20, default='preventive')
    schedule = models.ForeignKey(MaintenanceSchedule, on_delete=models.SET_NULL, null=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    problem_description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, default='medium', choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, default='open', choices=STATUS_CHOICES)
    assigned_technician = models.CharField(max_length=100, blank=True)
    assigned_team = models.CharField(max_length=200, blank=True)
    planned_start = models.DateTimeField(null=True)
    planned_end = models.DateTimeField(null=True)
    actual_start = models.DateTimeField(null=True)
    actual_end = models.DateTimeField(null=True)
    downtime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_cost = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    completion_notes = models.TextField(blank=True)
    root_cause = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_wo')
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='closed_wo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mnt_work_orders'
        ordering = ['-wo_date', '-created_at']

    def __str__(self):
        return self.wo_no


class WorkOrderTask(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='tasks')
    task_description = models.CharField(max_length=200)
    sequence_no = models.IntegerField(default=0)
    check_type = models.CharField(max_length=20, default='visual')
    expected_value = models.CharField(max_length=100, blank=True)
    actual_value = models.CharField(max_length=100, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_by = models.CharField(max_length=100, blank=True)
    completed_at = models.DateTimeField(null=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'mnt_wo_tasks'


class Breakdown(models.Model):
    STATUS_CHOICES = [
        ('reported', 'Reported'), ('investigating', 'Investigating'),
        ('repairing', 'Repairing'), ('resolved', 'Resolved'), ('closed', 'Closed')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    breakdown_no = models.CharField(max_length=100, unique=True)
    breakdown_date = models.DateTimeField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    reported_by = models.CharField(max_length=100, blank=True)
    problem_description = models.TextField()
    breakdown_type = models.CharField(max_length=20, default='mechanical')
    severity = models.CharField(max_length=20, default='major')
    downtime_start = models.DateTimeField(null=True)
    downtime_end = models.DateTimeField(null=True)
    total_downtime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    production_loss = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True)
    root_cause = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    preventive_action = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='reported', choices=STATUS_CHOICES)
    resolved_by = models.CharField(max_length=100, blank=True)
    resolved_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'mnt_breakdowns'


class SparePart(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_no = models.CharField(max_length=100, unique=True)
    part_name = models.CharField(max_length=200)
    part_description = models.TextField(blank=True)
    compatible_assets = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    supplier = models.CharField(max_length=200, blank=True)
    unit_cost = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    min_stock_level = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    max_stock_level = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    current_stock = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    storage_location = models.CharField(max_length=200, blank=True)
    lead_time_days = models.IntegerField(default=7)
    is_critical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'mnt_spare_parts'

    def __str__(self):
        return f"{self.part_no} - {self.part_name}"