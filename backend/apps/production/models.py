from django.db import models
from apps.inventory.models import StockItem
from apps.core.models import User
import uuid


class WorkCenter(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_center_code = models.CharField(max_length=50, unique=True)
    work_center_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    supervisor = models.CharField(max_length=100, blank=True)
    capacity_per_day = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    capacity_uom = models.CharField(max_length=50, default='Hours')
    cost_per_hour = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    overhead_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'prd_work_centers'

    def __str__(self):
        return self.work_center_name


class Machine(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    machine_code = models.CharField(max_length=50, unique=True)
    machine_name = models.CharField(max_length=200)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.SET_NULL, null=True)
    machine_type = models.CharField(max_length=100, blank=True)
    capacity_per_hour = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    power_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_maintenance_date = models.DateField(null=True)
    next_maintenance_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'prd_machines'

    def __str__(self):
        return self.machine_name


class Operation(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operation_code = models.CharField(max_length=50, unique=True)
    operation_name = models.CharField(max_length=200)
    work_center = models.ForeignKey(WorkCenter, on_delete=models.SET_NULL, null=True)
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    standard_time_minutes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    setup_time_minutes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_required = models.IntegerField(default=1)
    cost_per_operation = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'prd_operations'

    def __str__(self):
        return self.operation_name


class BOMHeader(models.Model):
    BOM_TYPES = [
        ('manufacturing', 'Manufacturing'), ('assembly', 'Assembly'),
        ('packing', 'Packing'), ('subcontract', 'Subcontract')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bom_no = models.CharField(max_length=100, unique=True)
    bom_name = models.CharField(max_length=200)
    finished_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='boms')
    finished_item_name = models.CharField(max_length=200)
    finished_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=1)
    finished_uom = models.CharField(max_length=50, default='Nos')
    bom_type = models.CharField(max_length=20, default='manufacturing', choices=BOM_TYPES)
    version = models.CharField(max_length=20, default='1.0')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    effective_from = models.DateField(null=True)
    effective_to = models.DateField(null=True)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prd_bom_header'

    def __str__(self):
        return self.bom_name


class BOMItem(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bom = models.ForeignKey(BOMHeader, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    required_quantity = models.DecimalField(max_digits=15, decimal_places=4)
    uom = models.CharField(max_length=50, blank=True)
    scrap_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    operation_sequence = models.IntegerField(default=0)
    is_critical = models.BooleanField(default=False)
    cost_per_unit = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    total_cost = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    class Meta:
        db_table = 'prd_bom_items'


class ProductionOrder(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'), ('released', 'Released'), ('in_progress', 'In Progress'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('on_hold', 'On Hold')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_no = models.CharField(max_length=100, unique=True)
    order_date = models.DateField()
    bom = models.ForeignKey(BOMHeader, on_delete=models.CASCADE)
    finished_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    finished_item_name = models.CharField(max_length=200)
    planned_quantity = models.DecimalField(max_digits=15, decimal_places=4)
    produced_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    rejected_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    target_godown = models.CharField(max_length=100, blank=True)
    planned_start_date = models.DateField(null=True)
    planned_end_date = models.DateField(null=True)
    actual_start_date = models.DateField(null=True)
    actual_end_date = models.DateField(null=True)
    priority = models.CharField(max_length=10, default='medium', choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, default='planned', choices=STATUS_CHOICES)
    sales_order_ref = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prd_orders'
        ordering = ['-order_date']

    def __str__(self):
        return self.order_no


class ProductionOutput(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    output_no = models.CharField(max_length=100, unique=True)
    output_date = models.DateField()
    order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    produced_quantity = models.DecimalField(max_digits=15, decimal_places=4)
    accepted_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    rejected_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    godown = models.ForeignKey('inventory.Godown', on_delete=models.SET_NULL, null=True)
    batch_no = models.CharField(max_length=100, blank=True)
    cost_per_unit = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    total_cost = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='pending')
    inspected_by = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'prd_output'


class QualityInspection(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection_no = models.CharField(max_length=100, unique=True)
    inspection_date = models.DateField()
    output = models.ForeignKey(ProductionOutput, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(ProductionOrder, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(StockItem, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200, blank=True)
    total_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    accepted_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    rejected_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    rework_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    rejection_reason = models.CharField(max_length=255, blank=True)
    inspection_result = models.CharField(max_length=20, default='passed')
    inspected_by = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'prd_quality_inspection'