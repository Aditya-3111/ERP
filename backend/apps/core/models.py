from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class FinancialYear(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_financial_years'
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class CompanyProfile(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default='India')
    gstin = models.CharField(max_length=15, blank=True)
    pan = models.CharField(max_length=10, blank=True)
    tan = models.CharField(max_length=10, blank=True)
    cin = models.CharField(max_length=21, blank=True)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_company_profile'

    def __str__(self):
        return self.company_name


class Branch(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    gstin = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_branches'

    def __str__(self):
        return self.name


class Role(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_roles'

    def __str__(self):
        return self.label


class User(AbstractUser):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    status = models.CharField(max_length=20, default='active', choices=[
        ('active', 'Active'), ('inactive', 'Inactive')
    ])
    login_attempts = models.IntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'core_users'

    def __str__(self):
        return self.get_full_name() or self.username


class UserSession(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_user_sessions'


class SystemSetting(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    setting_type = models.CharField(max_length=20, default='text', choices=[
        ('text', 'Text'), ('number', 'Number'), ('boolean', 'Boolean'), ('json', 'JSON')
    ])
    description = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_system_settings'

    def __str__(self):
        return self.key


class AuditLog(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'core_audit_logs'
        ordering = ['-created_at']