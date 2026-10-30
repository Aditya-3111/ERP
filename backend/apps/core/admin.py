from django.contrib import admin
from apps.core.models import (
    FinancialYear, CompanyProfile, Branch, Role, SystemSetting,
    User, AuditLog, UserSession
)

@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active', 'is_locked']
    list_filter = ['is_active', 'is_locked']
    search_fields = ['name']

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'city', 'state', 'gstin']
    search_fields = ['company_name', 'gstin']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'city', 'state', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'is_system']
    list_filter = ['is_system']
    search_fields = ['name', 'label']

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'setting_type', 'updated_at']
    list_filter = ['setting_type']
    search_fields = ['key']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'status', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'status', 'role']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filter_horizontal = ['groups', 'user_permissions']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['username', 'action', 'module', 'created_at']
    list_filter = ['action', 'module']
    search_fields = ['username', 'action', 'module']
    date_hierarchy = 'created_at'

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'expires_at', 'created_at']
    list_filter = ['user']
    search_fields = ['user__username', 'ip_address']
