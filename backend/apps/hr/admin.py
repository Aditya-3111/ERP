from django.contrib import admin
from apps.hr.models import Department, Designation, Employee, Attendance, PayHead, EmployeeDocument

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_code', 'name', 'department', 'designation', 'status']
    list_filter = ['status', 'department', 'designation']
    search_fields = ['emp_code', 'name', 'mobile']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'in_time', 'out_time', 'status']
    list_filter = ['status']
    search_fields = ['employee__name']
    date_hierarchy = 'date'

@admin.register(PayHead)
class PayHeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'pay_type', 'calculation_type']
    list_filter = ['pay_type', 'calculation_type']
    search_fields = ['name']

@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'document_type', 'document_name']
    list_filter = ['document_type']
    search_fields = ['employee__name', 'document_name']
