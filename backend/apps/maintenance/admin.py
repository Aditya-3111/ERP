from django.contrib import admin
from apps.maintenance.models import (
    AssetCategory, Asset, MaintenanceSchedule, WorkOrder,
    WorkOrderTask, Breakdown, SparePart
)

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_code', 'parent', 'depreciation_rate', 'is_active']
    list_filter = ['is_active']
    search_fields = ['category_name', 'category_code']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_code', 'asset_name', 'category', 'status', 'criticality', 'current_value']
    list_filter = ['status', 'criticality', 'category']
    search_fields = ['asset_code', 'asset_name']

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ['schedule_name', 'asset', 'frequency_type', 'next_due_date', 'status']
    list_filter = ['status', 'frequency_type']
    search_fields = ['schedule_name', 'asset__asset_name']
    date_hierarchy = 'next_due_date'

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['wo_no', 'asset', 'problem_description', 'priority', 'status']
    list_filter = ['status', 'priority']
    search_fields = ['wo_no', 'asset__asset_name']
    date_hierarchy = 'wo_date'

@admin.register(WorkOrderTask)
class WorkOrderTaskAdmin(admin.ModelAdmin):
    list_display = ['work_order', 'task_description', 'sequence_no', 'is_completed']
    list_filter = ['is_completed']
    search_fields = ['task_description', 'work_order__wo_no']

@admin.register(Breakdown)
class BreakdownAdmin(admin.ModelAdmin):
    list_display = ['breakdown_no', 'asset', 'breakdown_type', 'severity', 'status']
    list_filter = ['status', 'breakdown_type', 'severity']
    search_fields = ['breakdown_no', 'asset__asset_name']
    date_hierarchy = 'breakdown_date'

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['part_name', 'part_no', 'current_stock', 'min_stock_level', 'is_critical', 'is_active']
    list_filter = ['is_critical', 'is_active']
    search_fields = ['part_name', 'part_no']
