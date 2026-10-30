from django.db import models
import uuid


class Department(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_departments'

    def __str__(self):
        return self.name


class Designation(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'hr_designations'

    def __str__(self):
        return self.name


class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'), ('inactive', 'Inactive'),
        ('resigned', 'Resigned'), ('terminated', 'Terminated')
    ]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    function_role = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    father_mother_name = models.CharField(max_length=200, blank=True)
    spouse_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    pan = models.CharField(max_length=10, blank=True)
    aadhaar = models.CharField(max_length=12, blank=True)
    uan = models.CharField(max_length=20, blank=True)
    pf_number = models.CharField(max_length=50, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    date_of_release = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=17, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='active', choices=STATUS_CHOICES)
    photo = models.ImageField(upload_to='employees/', blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_employees'

    def __str__(self):
        return f"{self.emp_code} - {self.name}"


class EmployeeDocument(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    document_name = models.CharField(max_length=200)
    document_file = models.FileField(upload_to='employee_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_employee_documents'


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'), ('Absent', 'Absent'), ('Half Day', 'Half Day'),
        ('Leave', 'Leave'), ('Holiday', 'Holiday')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, default='Present', choices=STATUS_CHOICES)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hr_attendance'
        unique_together = ['employee', 'date']


class PayHead(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    parent = models.CharField(max_length=200, blank=True)
    payslip_name = models.CharField(max_length=200, blank=True)
    pay_type = models.CharField(max_length=20, choices=[('Earning', 'Earning'), ('Deduction', 'Deduction')])
    income_type = models.CharField(max_length=50, blank=True)
    calculation_type = models.CharField(max_length=50, blank=True)
    leave_type = models.CharField(max_length=50, blank=True)
    calculation_period = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'hr_pay_heads'

    def __str__(self):
        return self.name