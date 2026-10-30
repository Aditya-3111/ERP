from django.contrib import admin
from apps.production.models import WorkCenter, Machine, Operation, BOMHeader, BOMItem, ProductionOrder, ProductionOutput, QualityInspection

@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    list_display = ['work_center_name', 'work_center_code', 'department', 'is_active']
    list_filter = ['is_active']
    search_fields = ['work_center_name', 'work_center_code']

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['machine_name', 'machine_code', 'work_center', 'is_active']
    list_filter = ['is_active']
    search_fields = ['machine_name', 'machine_code']

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['operation_name', 'operation_code', 'work_center', 'standard_time_minutes']
    list_filter = ['work_center']
    search_fields = ['operation_name', 'operation_code']

@admin.register(BOMHeader)
class BOMHeaderAdmin(admin.ModelAdmin):
    list_display = ['bom_name', 'bom_no', 'finished_item', 'bom_type', 'is_active', 'is_default']
    list_filter = ['bom_type', 'is_active', 'is_default']
    search_fields = ['bom_name', 'bom_no', 'finished_item__name']

@admin.register(BOMItem)
class BOMItemAdmin(admin.ModelAdmin):
    list_display = ['bom', 'item', 'required_quantity', 'uom', 'is_critical']
    list_filter = ['is_critical']
    search_fields = ['item__name', 'bom__bom_name']

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'bom', 'planned_quantity', 'produced_quantity', 'status', 'priority']
    list_filter = ['status', 'priority']
    search_fields = ['order_no', 'bom__bom_name']
    date_hierarchy = 'order_date'

@admin.register(ProductionOutput)
class ProductionOutputAdmin(admin.ModelAdmin):
    list_display = ['output_no', 'order', 'item', 'produced_quantity', 'accepted_quantity', 'status']
    list_filter = ['status']
    search_fields = ['output_no', 'order__order_no']
    date_hierarchy = 'output_date'

@admin.register(QualityInspection)
class QualityInspectionAdmin(admin.ModelAdmin):
    list_display = ['inspection_no', 'output', 'item', 'total_quantity', 'accepted_quantity', 'inspection_result']
    list_filter = ['inspection_result']
    search_fields = ['inspection_no', 'output__output_no']
    date_hierarchy = 'inspection_date'
