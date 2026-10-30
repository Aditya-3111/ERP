from django.contrib import admin
from apps.gate.models import Visitor, VisitorLog, GateEntry, Transporter

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'id_proof_type', 'id_proof_number', 'company', 'purpose', 'status']
    list_filter = ['status', 'purpose', 'id_proof_type']
    search_fields = ['name', 'mobile', 'id_proof_number', 'company']

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'visitor_name', 'action', 'timestamp']
    list_filter = ['action']
    search_fields = ['visitor__name', 'visitor_name']
    date_hierarchy = 'timestamp'

@admin.register(GateEntry)
class GateEntryAdmin(admin.ModelAdmin):
    list_display = ['gate_pass_no', 'date', 'type', 'vehicle_no', 'driver_name', 'party_name', 'status']
    list_filter = ['type', 'status']
    search_fields = ['gate_pass_no', 'vehicle_no', 'driver_name', 'party_name']
    date_hierarchy = 'date'

@admin.register(Transporter)
class TransporterAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'address', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'contact']
