from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import Role, FinancialYear, Branch
import uuid

User = get_user_model()


# ============================================
# 1. MODULE REGISTRY
# ============================================
class RegisteredModule(models.Model):
    """Modules registered in the system"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module_key = models.CharField(max_length=50, unique=True)
    module_name = models.CharField(max_length=100)
    module_icon = models.CharField(max_length=50, blank=True)
    module_description = models.TextField(blank=True)
    module_url = models.CharField(max_length=200, blank=True)
    parent_module = models.CharField(max_length=50, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_core = models.BooleanField(default=False)
    version = models.CharField(max_length=20, default='1.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_modules'
        ordering = ['sort_order']

    def __str__(self):
        return self.module_name


class ModuleSetting(models.Model):
    """Per-module configuration settings"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(RegisteredModule, on_delete=models.CASCADE, related_name='settings')
    setting_key = models.CharField(max_length=100)
    setting_value = models.TextField(blank=True)
    setting_type = models.CharField(max_length=20, default='text', choices=[
        ('text', 'Text'), ('number', 'Number'),
        ('boolean', 'Boolean'), ('json', 'JSON'), ('file', 'File')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_module_settings'
        unique_together = ['module', 'setting_key']

    def __str__(self):
        return f"{self.module.module_name} - {self.setting_key}"


# ============================================
# 2. MENU MANAGEMENT
# ============================================
class MenuGroup(models.Model):
    """Sidebar menu groups"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_key = models.CharField(max_length=50, unique=True)
    group_label = models.CharField(max_length=100)
    group_icon = models.CharField(max_length=50, blank=True)
    sort_order = models.IntegerField(default=0)
    is_default_open = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_menu_groups'
        ordering = ['sort_order']

    def __str__(self):
        return self.group_label


class MenuItem(models.Model):
    """Sidebar menu items"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(MenuGroup, on_delete=models.CASCADE, related_name='items')
    item_key = models.CharField(max_length=50)
    item_label = models.CharField(max_length=100)
    item_icon = models.CharField(max_length=50, blank=True)
    item_page = models.CharField(max_length=100)
    item_url = models.CharField(max_length=200, blank=True)
    parent_item = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    required_permission = models.CharField(max_length=50, blank=True)
    badge_text = models.CharField(max_length=50, blank=True)
    badge_color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_menu_items'
        ordering = ['sort_order']
        unique_together = ['group', 'item_key']

    def __str__(self):
        return self.item_label


# ============================================
# 3. PERMISSIONS & ACCESS CONTROL
# ============================================
class PermissionGroup(models.Model):
    """Group of related permissions"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=100)
    group_key = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_permission_groups'

    def __str__(self):
        return self.group_name


class Permission(models.Model):
    """Individual permissions"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_key = models.CharField(max_length=100, unique=True)
    permission_name = models.CharField(max_length=200)
    permission_group = models.ForeignKey(PermissionGroup, on_delete=models.SET_NULL, null=True, related_name='permissions')
    module = models.ForeignKey(RegisteredModule, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_permissions'

    def __str__(self):
        return self.permission_name


class RolePermission(models.Model):
    """Role-Permission mapping"""
    ACCESS_LEVELS = [
        ('deny', 'Deny'), ('read', 'Read'),
        ('write', 'Write'), ('delete', 'Delete'), ('full', 'Full')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, default='read', choices=ACCESS_LEVELS)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_permissions')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_role_permissions'
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.label} - {self.permission.permission_name}"


class UserPermission(models.Model):
    """Individual user permission overrides"""
    ACCESS_LEVELS = [
        ('deny', 'Deny'), ('read', 'Read'),
        ('write', 'Write'), ('delete', 'Delete'), ('full', 'Full')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, default='read', choices=ACCESS_LEVELS)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_admin_user_permissions')
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'admin_user_permissions'
        unique_together = ['user', 'permission']

    def __str__(self):
        return f"{self.user.username} - {self.permission.permission_name}"


# ============================================
# 4. DATA BACKUP & RESTORE
# ============================================
class DataBackup(models.Model):
    """System backup records"""
    BACKUP_TYPES = [
        ('full', 'Full Backup'), ('partial', 'Partial Backup'),
        ('automatic', 'Automatic Backup')
    ]
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    backup_name = models.CharField(max_length=200)
    backup_type = models.CharField(max_length=20, default='full', choices=BACKUP_TYPES)
    backup_size = models.BigIntegerField(default=0)
    backup_file = models.FileField(upload_to='backups/', blank=True)
    tables_backed_up = models.TextField(blank=True)
    records_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='completed', choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_backups'
        ordering = ['-created_at']

    def __str__(self):
        return self.backup_name


class DataRestore(models.Model):
    """System restore records"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    backup = models.ForeignKey(DataBackup, on_delete=models.CASCADE, related_name='restores')
    restore_type = models.CharField(max_length=20, default='full', choices=[('full', 'Full'), ('partial', 'Partial')])
    status = models.CharField(max_length=20, default='completed', choices=STATUS_CHOICES)
    restored_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    restored_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = 'admin_restores'

    def __str__(self):
        return f"Restore from {self.backup.backup_name}"


# ============================================
# 5. SYSTEM MONITORING & LOGS
# ============================================
class SystemLog(models.Model):
    """System-level logs"""
    LOG_LEVELS = [
        ('INFO', 'Info'), ('WARNING', 'Warning'),
        ('ERROR', 'Error'), ('CRITICAL', 'Critical')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    log_level = models.CharField(max_length=10, default='INFO', choices=LOG_LEVELS)
    log_module = models.CharField(max_length=100, blank=True)
    log_message = models.TextField()
    log_details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_system_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['log_level']),
            models.Index(fields=['log_module']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"[{self.log_level}] {self.log_module}"


class DatabaseStatistic(models.Model):
    """Database table statistics"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_name = models.CharField(max_length=100)
    record_count = models.IntegerField(default=0)
    table_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_db_statistics'
        ordering = ['table_name']

    def __str__(self):
        return self.table_name


# ============================================
# 6. SCHEDULED TASKS / CRON JOBS
# ============================================
class ScheduledTask(models.Model):
    """Automated system tasks"""
    STATUS_CHOICES = [
        ('active', 'Active'), ('paused', 'Paused'),
        ('completed', 'Completed'), ('failed', 'Failed')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=200)
    task_key = models.CharField(max_length=100, unique=True)
    task_description = models.TextField(blank=True)
    cron_expression = models.CharField(max_length=50, blank=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active', choices=STATUS_CHOICES)
    run_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_scheduled_tasks'

    def __str__(self):
        return self.task_name


class TaskExecutionHistory(models.Model):
    """Execution history of scheduled tasks"""
    STATUS_CHOICES = [
        ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(ScheduledTask, on_delete=models.CASCADE, related_name='executions')
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
    duration_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='running', choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_task_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task.task_name} - {self.status}"


# ============================================
# 7. EMAIL & NOTIFICATIONS
# ============================================
class EmailTemplate(models.Model):
    """Email templates for system notifications"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_key = models.CharField(max_length=100, unique=True)
    template_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    body_html = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    variables = models.JSONField(default=dict, blank=True, help_text="Available variables for this template")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_email_templates'

    def __str__(self):
        return self.template_name


class EmailQueue(models.Model):
    """Outgoing email queue"""
    PRIORITY_CHOICES = [('low', 'Low'), ('normal', 'Normal'), ('high', 'High')]
    STATUS_CHOICES = [('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')]

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    to_email = models.EmailField()
    cc_email = models.TextField(blank=True)
    bcc_email = models.TextField(blank=True)
    subject = models.CharField(max_length=255)
    body_html = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    attachments = models.JSONField(default=list, blank=True)
    priority = models.CharField(max_length=10, default='normal', choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_email_queue'
        ordering = ['-priority', 'created_at']

    def __str__(self):
        return f"Email to {self.to_email} - {self.subject}"


class Notification(models.Model):
    """In-app notifications"""
    NOTIFICATION_TYPES = [
        ('info', 'Information'), ('success', 'Success'),
        ('warning', 'Warning'), ('error', 'Error')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, default='info', choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title


# ============================================
# 8. CONFIGURATION PRESETS
# ============================================
class ConfigurationPreset(models.Model):
    """Saveable configuration presets"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    preset_name = models.CharField(max_length=200)
    preset_key = models.CharField(max_length=100, unique=True)
    preset_description = models.TextField(blank=True)
    preset_data = models.JSONField(default=dict)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_config_presets'

    def __str__(self):
        return self.preset_name


# ============================================
# 9. LICENSE & ACTIVATION
# ============================================
class License(models.Model):
    """Software license information"""
    LICENSE_TYPES = [
        ('trial', 'Trial'), ('basic', 'Basic'),
        ('professional', 'Professional'), ('enterprise', 'Enterprise')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_key = models.CharField(max_length=255, unique=True)
    license_type = models.CharField(max_length=20, default='trial', choices=LICENSE_TYPES)
    licensed_to = models.CharField(max_length=200, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_users = models.IntegerField(default=5)
    max_companies = models.IntegerField(default=1)
    max_branches = models.IntegerField(default=1)
    features = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_license'

    def __str__(self):
        return f"{self.license_type} - {self.licensed_to}"


# ============================================
# 10. IP WHITELIST / SECURITY
# ============================================
class IPWhitelist(models.Model):
    """IP addresses allowed to access the system"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(unique=True)
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_ip_whitelist'

    def __str__(self):
        return self.ip_address


class LoginAttempt(models.Model):
    """Track login attempts for security"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    is_successful = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_login_attempts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username', 'created_at']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return f"{self.username} - {'Success' if self.is_successful else 'Failed'}"


# ============================================
# 11. API TOKENS / WEBHOOKS
# ============================================
class APIToken(models.Model):
    """API access tokens for third-party integration"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_tokens')
    token_name = models.CharField(max_length=100)
    token_key = models.CharField(max_length=255, unique=True)
    token_secret = models.CharField(max_length=255)
    scopes = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_api_tokens'

    def __str__(self):
        return f"{self.token_name} - {self.user.username}"


class Webhook(models.Model):
    """Webhook endpoints for event notifications"""
    EVENT_CHOICES = [
        ('voucher.created', 'Voucher Created'),
        ('voucher.updated', 'Voucher Updated'),
        ('customer.created', 'Customer Created'),
        ('invoice.generated', 'Invoice Generated'),
        ('payment.received', 'Payment Received'),
        ('stock.low', 'Low Stock Alert'),
        ('user.login', 'User Login'),
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    webhook_name = models.CharField(max_length=200)
    webhook_url = models.URLField()
    events = models.JSONField(default=list, help_text="List of events to trigger webhook")
    secret_key = models.CharField(max_length=255, blank=True)
    headers = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    failure_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_webhooks'

    def __str__(self):
        return self.webhook_name


class WebhookLog(models.Model):
    """Webhook execution logs"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='logs')
    event = models.CharField(max_length=50)
    request_body = models.JSONField(default=dict, blank=True)
    response_status = models.IntegerField(null=True)
    response_body = models.TextField(blank=True)
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    duration_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_webhook_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.webhook.webhook_name} - {self.event}"


# ============================================
# 12. ACTIVITY / NEWS FEED
# ============================================
class ActivityFeed(models.Model):
    """System-wide activity feed"""
    ACTIVITY_TYPES = [
        ('create', 'Created'), ('update', 'Updated'), ('delete', 'Deleted'),
        ('login', 'Logged In'), ('logout', 'Logged Out'), ('export', 'Exported'),
        ('import', 'Imported'), ('backup', 'Backed Up'), ('restore', 'Restored')
    ]
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=150)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    module = models.CharField(max_length=100)
    description = models.TextField()
    reference_id = models.CharField(max_length=64, blank=True)
    reference_type = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_activity_feed'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['module']),
            models.Index(fields=['activity_type']),
        ]

    def __str__(self):
        return f"{self.username} {self.activity_type}d {self.module}"


# ============================================
# 13. MAINTENANCE MODE
# ============================================
class MaintenanceMode(models.Model):
    """System maintenance mode settings"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_enabled = models.BooleanField(default=False)
    title = models.CharField(max_length=200, default='System Under Maintenance')
    message = models.TextField(default='We are currently performing scheduled maintenance. Please check back soon.')
    allowed_ips = models.JSONField(default=list, blank=True)
    allowed_users = models.ManyToManyField(User, blank=True, related_name='maintenance_access')
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_set_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_maintenance_mode'

    def __str__(self):
        return "Maintenance Mode"


# ============================================
# 14. THEME & APPEARANCE
# ============================================
class ThemeSettings(models.Model):
    """UI Theme customization"""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='theme_settings')
    theme_mode = models.CharField(max_length=10, default='light', choices=[
        ('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')
    ])
    primary_color = models.CharField(max_length=20, default='#1a237e')
    accent_color = models.CharField(max_length=20, default='#ff6f00')
    font_size = models.CharField(max_length=10, default='13px')
    sidebar_collapsed = models.BooleanField(default=False)
    layout_density = models.CharField(max_length=15, default='comfortable', choices=[
        ('compact', 'Compact'), ('comfortable', 'Comfortable'), ('spacious', 'Spacious')
    ])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_theme_settings'

    def __str__(self):
        return f"Theme - {self.user.username}"