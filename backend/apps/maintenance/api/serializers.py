from rest_framework import serializers
from apps.maintenance.models import (Breakdown, AssetCategory, Asset, MaintenanceSchedule,
                                 WorkOrder, WorkOrderTask)
import uuid

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = ['guid', 'category_name', 'category_code', 'parent', 
                 'depreciation_rate', 'depreciation_method', 
                 'useful_life_years', 'is_active']
        read_only_fields = ['guid']

class AssetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    
    class Meta:
        model = Asset
        fields = ['guid', 'asset_code', 'asset_name', 'category', 'category_name',
                 'asset_type', 'model_no', 'serial_no', 'manufacturer', 
                 'supplier', 'purchase_date', 'purchase_price', 
                 'warranty_start', 'warranty_end', 'current_value',
                 'location', 'department', 'responsible_person', 
                 'criticality', 'status', 'barcode', 'specifications', 
                 'remarks']
        read_only_fields = ['guid', 'current_value']

class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.asset_name', read_only=True)
    
    class Meta:
        model = MaintenanceSchedule
        fields = ['guid', 'schedule_name', 'schedule_code', 'asset', 'asset_name',
                 'frequency_type', 'frequency_value', 'last_performed_date',
                 'next_due_date', 'estimated_duration_hours', 'estimated_cost',
                 'assigned_technician', 'priority', 'status', 'start_date',
                 'end_date', 'remarks']
        read_only_fields = ['guid']

class WorkOrderSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.asset_name', read_only=True)
    
    class Meta:
        model = WorkOrder
        fields = ['guid', 'wo_no', 'wo_date', 'wo_type', 'schedule', 'asset',
                 'asset_name', 'problem_description', 'priority', 'status',
                 'assigned_technician', 'assigned_team', 'planned_start',
                 'planned_end', 'actual_start', 'actual_end', 'downtime_hours',
                 'estimated_cost', 'actual_cost', 'completion_notes',
                 'root_cause', 'corrective_action']
        read_only_fields = ['guid']

class WorkOrderTaskSerializer(serializers.ModelSerializer):
    wo_no = serializers.CharField(source='work_order.wo_no', read_only=True)
    
    class Meta:
        model = WorkOrderTask
        fields = ['guid', 'work_order', 'wo_no', 'task_description',
                 'sequence_no', 'check_type', 'expected_value', 'actual_value',
                 'is_completed', 'completed_by', 'completed_at', 'remarks']
        read_only_fields = ['guid']


class BreakdownSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)

    class Meta:
        model = Breakdown
        fields = '__all__'
        read_only_fields = ['guid']
