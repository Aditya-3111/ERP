from rest_framework import serializers
from apps.inventory.models import (UnitOfMeasure, StockGroup, StockCategory, 
                             Godown, StockItem, StockBatch, StockJournal, 
                             MaterialReceiptNote, MRNItem)
import uuid

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['guid', 'name', 'formal_name', 'is_simple_unit', 
                 'base_units', 'additional_units', 'conversion']
        read_only_fields = ['guid']

class StockGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockGroup
        fields = ['guid', 'name', 'parent']
        read_only_fields = ['guid']

class StockCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCategory
        fields = ['guid', 'name', 'parent']
        read_only_fields = ['guid']

class GodownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Godown
        fields = ['guid', 'name', 'parent', 'address', 'city', 
                 'state', 'pincode', 'incharge', 'mobile', 'is_active']
        read_only_fields = ['guid']

class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = ['guid', 'name', 'parent', 'category', 'alias', 'description',
                 'part_number', 'uom', 'alternate_uom', 'conversion',
                 'opening_balance', 'opening_rate', 'opening_value',
                 'closing_balance', 'closing_rate', 'closing_value',
                 'costing_method', 'default_godown', 'min_stock', 'max_stock',
                 'gst_type_of_supply', 'gst_hsn_code', 'gst_hsn_description',
                 'gst_rate', 'gst_taxability', 'is_active']
        read_only_fields = ['guid', 'closing_balance', 'closing_rate',
                           'closing_value']

class StockBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBatch
        fields = ['guid', 'item', 'item_name', 'batch_no', 'mfg_date',
                 'exp_date', 'quantity', 'godown']
        read_only_fields = ['guid']

class StockJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockJournal
        fields = ['guid', 'date', 'item', 'item_name', 'type',
                 'quantity', 'rate', 'godown', 'destination_godown', 'reference']
        read_only_fields = ['guid']

class MaterialReceiptNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialReceiptNote
        fields = ['guid', 'mrn_no', 'date', 'supplier_name', 'supplier_invoice',
                 'transporter', 'vehicle_no', 'godown', 'eway_bill', 'remarks', 'status']
        read_only_fields = ['guid']
