from rest_framework import serializers
from apps.gate.models import Visitor, Transporter, GateEntry, VisitorLog
import uuid

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['guid', 'visitor_id', 'name', 'company', 'designation',
                 'mobile', 'email', 'gender', 'id_proof_type', 'id_proof_number',
                 'purpose', 'host_employee', 'host_department', 'entry_date',
                 'entry_time', 'exit_time', 'expected_duration', 'no_of_persons',
                 'vehicle_no', 'vehicle_type', 'belongings', 'visitor_category',
                 'badge_no', 'security_by', 'nda_signed', 'safety_briefing',
                 'photo', 'status', 'remarks']
        read_only_fields = ['guid']

class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = ['guid', 'name', 'contact', 'address', 'is_active']
        read_only_fields = ['guid']

class GateEntrySerializer(serializers.ModelSerializer):
    party_name_display = serializers.CharField(source='party_name', read_only=True)
    transporter_name = serializers.CharField(source='transporter.name', read_only=True)
    
    class Meta:
        model = GateEntry
        fields = ['guid', 'gate_pass_no', 'date', 'time', 'type', 
                 'vehicle_no', 'vehicle_type', 'transporter', 'party_name',
                 'party_name_display', 'transporter_name', 'material', 
                 'quantity', 'uom', 'challan_no', 'driver_name', 
                 'driver_mobile', 'security_check', 'exit_time', 'status', 
                 'remarks']
        read_only_fields = ['guid']

class VisitorLogSerializer(serializers.ModelSerializer):
    visitor_name = serializers.CharField(source='visitor.name', read_only=True)
    
    class Meta:
        model = VisitorLog
        fields = ['guid', 'visitor', 'visitor_name', 'action', 'timestamp', 'details']
        read_only_fields = ['guid']
