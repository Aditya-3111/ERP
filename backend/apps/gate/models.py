from django.db import models
import uuid


class Visitor(models.Model):
    STATUS_CHOICES = [('checked_in', 'Checked In'), ('checked_out', 'Checked Out')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    id_proof_type = models.CharField(max_length=50, blank=True)
    id_proof_number = models.CharField(max_length=50, blank=True)
    id_proof_file = models.FileField(upload_to='visitors/id_proof/', blank=True)
    purpose = models.CharField(max_length=100)
    host_employee = models.CharField(max_length=200)
    host_department = models.CharField(max_length=100, blank=True)
    entry_date = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField(null=True, blank=True)
    expected_duration = models.IntegerField(default=60)
    no_of_persons = models.IntegerField(default=1)
    vehicle_no = models.CharField(max_length=20, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    belongings = models.CharField(max_length=255, blank=True)
    visitor_category = models.CharField(max_length=50, default='General')
    badge_no = models.CharField(max_length=50, blank=True)
    security_by = models.CharField(max_length=100, blank=True)
    nda_signed = models.BooleanField(default=False)
    safety_briefing = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='visitors/photos/', blank=True)
    qr_code = models.ImageField(upload_to='visitors/qr/', blank=True)
    status = models.CharField(max_length=20, default='checked_in', choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gate_visitors'
        ordering = ['-entry_date', '-entry_time']

    def __str__(self):
        return f"{self.visitor_id} - {self.name}"


class VisitorLog(models.Model):
    ACTION_CHOICES = [('CHECK_IN', 'Check In'), ('CHECK_OUT', 'Check Out')]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=200)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        db_table = 'gate_visitor_logs'


class GateEntry(models.Model):
    TYPE_CHOICES = [('INWARD', 'Inward'), ('OUTWARD', 'Outward')]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('AT_GATE', 'At Gate'), ('COMPLETED', 'Completed')]

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gate_pass_no = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    vehicle_no = models.CharField(max_length=20, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    transporter = models.CharField(max_length=200, blank=True)
    party_name = models.CharField(max_length=200, blank=True)
    material = models.CharField(max_length=200, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    uom = models.CharField(max_length=50, blank=True)
    challan_no = models.CharField(max_length=100, blank=True)
    driver_name = models.CharField(max_length=100, blank=True)
    driver_mobile = models.CharField(max_length=15, blank=True)
    security_check = models.CharField(max_length=100, blank=True)
    exit_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='AT_GATE', choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gate_entries'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.gate_pass_no} - {self.type}"


class Transporter(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'gate_transporters'

    def __str__(self):
        return self.name