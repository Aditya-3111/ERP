from rest_framework import serializers
from apps.production.models import (WorkCenter, Machine, Operation, 
                              BOMHeader, BOMItem, 
                              ProductionOrder, ProductionOutput, 
                              QualityInspection)
import uuid

class WorkCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkCenter
        fields = ['guid', 'work_center_code', 'work_center_name', 
                 'department', 'location', 'supervisor', 
                 'capacity_per_day', 'capacity_uom', 'cost_per_hour',
                 'overhead_percent', 'is_active']
        read_only_fields = ['guid']

class MachineSerializer(serializers.ModelSerializer):
    work_center_name = serializers.CharField(source='work_center.work_center_name', read_only=True)
    
    class Meta:
        model = Machine
        fields = ['guid', 'machine_code', 'machine_name', 'work_center', 
                 'work_center_name', 'machine_type', 'capacity_per_hour',
                 'power_consumption', 'last_maintenance_date',
                 'next_maintenance_date', 'is_active']
        read_only_fields = ['guid']

class OperationSerializer(serializers.ModelSerializer):
    work_center_name = serializers.CharField(source='work_center.work_center_name', read_only=True)
    
    class Meta:
        model = Operation
        fields = ['guid', 'operation_code', 'operation_name', 
                 'work_center', 'work_center_name', 'setup_time_minutes',
                 'standard_time_minutes', 'cost_per_operation', 'is_active']
        read_only_fields = ['guid']

class BOMHeaderSerializer(serializers.ModelSerializer):
    finished_item_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = BOMHeader
        fields = ['guid', 'bom_no', 'bom_name', 'finished_item', 'finished_item_name',
                 'finished_quantity', 'finished_uom', 'bom_type', 'version',
                 'is_active', 'is_default', 'effective_from', 'effective_to', 'remarks']
        read_only_fields = ['guid']

class BOMItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    bom_name = serializers.CharField(source='bom.bom_name', read_only=True)
    
    class Meta:
        model = BOMItem
        fields = ['guid', 'bom', 'bom_name', 'item', 'item_name',
                 'required_quantity', 'uom', 'scrap_percent',
                 'operation_sequence', 'is_critical', 'cost_per_unit', 'total_cost']
        read_only_fields = ['guid']

class ProductionOrderSerializer(serializers.ModelSerializer):
    bom_name = serializers.CharField(source='bom.bom_name', read_only=True)
    finished_item_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = ProductionOrder
        fields = ['guid', 'order_no', 'order_date', 'bom', 'bom_name',
                 'finished_item', 'finished_item_name', 'planned_quantity',
                 'produced_quantity', 'rejected_quantity', 'uom', 'target_godown',
                 'planned_start_date', 'planned_end_date', 'actual_start_date',
                 'actual_end_date', 'priority', 'status', 'sales_order_ref',
                 'remarks']
        read_only_fields = ['guid']

class ProductionOutputSerializer(serializers.ModelSerializer):
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    
    class Meta:
        model = ProductionOutput
        fields = ['guid', 'output_no', 'output_date', 'order', 'order_no',
                 'item', 'item_name', 'produced_quantity', 'accepted_quantity',
                 'rejected_quantity', 'uom', 'godown', 'batch_no',
                 'cost_per_unit', 'total_cost', 'status', 'inspected_by', 'remarks']
        read_only_fields = ['guid']

class QualityInspectionSerializer(serializers.ModelSerializer):
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    
    class Meta:
        model = QualityInspection
        fields = ['guid', 'inspection_no', 'inspection_date', 'output', 'order',
                 'order_no', 'item', 'item_name', 'total_quantity',
                 'accepted_quantity', 'rejected_quantity', 'rework_quantity',
                 'rejection_reason', 'inspection_result', 'inspected_by', 'remarks']
        read_only_fields = ['guid']
