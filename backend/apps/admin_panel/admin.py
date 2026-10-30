from django.contrib import admin
from apps.admin_panel.models import (
    RegisteredModule, ModuleSetting, MenuGroup, MenuItem,
    PermissionGroup, Permission, RolePermission, UserPermission,
    DataBackup, DataRestore, SystemLog, DatabaseStatistic,
    ScheduledTask, TaskExecutionHistory, EmailTemplate, EmailQueue,
    Notification, ConfigurationPreset, License, IPWhitelist,
    LoginAttempt, APIToken, Webhook, WebhookLog,
    ActivityFeed, MaintenanceMode, ThemeSettings
)


@admin.register(RegisteredModule)
class RegisteredModuleAdmin(admin.ModelAdmin):
    list_display = ['module_name', 'module_key', 'is_active', 'is_core', 'sort_order']
    list_filter = ['is_active', 'is_core']
    search_fields = ['module_name', 'module_key']


@admin.register(MenuGroup)
class MenuGroupAdmin(admin.ModelAdmin):
    list_display = ['group_label', 'group_key', 'sort_order', 'is_active', 'is_default_open']
    list_filter = ['is_active']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['item_label', 'group', 'item_page', 'sort_order', 'is_active']
    list_filter = ['group', 'is_active']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission_name', 'permission_key', 'permission_group', 'module']
    search_fields = ['permission_name', 'permission_key']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission', 'access_level']
    list_filter = ['role', 'access_level']


@admin.register(DataBackup)
class DataBackupAdmin(admin.ModelAdmin):
    list_display = ['backup_name', 'backup_type', 'status', 'records_count', 'created_at']
    list_filter = ['backup_type', 'status']


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['log_level', 'log_module', 'created_at']
    list_filter = ['log_level', 'log_module']
    search_fields = ['log_message']


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'status', 'last_run', 'next_run', 'run_count']
    list_filter = ['status']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_name', 'template_key', 'is_active']
    search_fields = ['template_name', 'subject']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ['license_type', 'licensed_to', 'expires_at', 'is_active']


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip_address', 'is_successful', 'created_at']
    list_filter = ['is_successful']


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['webhook_name', 'webhook_url', 'is_active', 'failure_count']
    list_filter = ['is_active']


@admin.register(MaintenanceMode)
class MaintenanceModeAdmin(admin.ModelAdmin):
    list_display = ['is_enabled', 'started_at', 'ended_at']


# Register remaining models
admin.site.register(ModuleSetting)
admin.site.register(UserPermission)
admin.site.register(DataRestore)
admin.site.register(DatabaseStatistic)
admin.site.register(TaskExecutionHistory)
admin.site.register(EmailQueue)
admin.site.register(ConfigurationPreset)
admin.site.register(IPWhitelist)
admin.site.register(APIToken)
admin.site.register(WebhookLog)
admin.site.register(ActivityFeed)
admin.site.register(ThemeSettings)
admin.site.register(PermissionGroup)