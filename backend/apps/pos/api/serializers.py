from rest_framework import serializers
from apps.pos.models import (POSCounter, POSSession, ItemPrice, POSSale, 
                          POSSaleItem, POSPayment, PaymentMethod, PriceList)
import uuid

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['guid', 'method_name', 'method_code', 'method_type', 'is_active']
        read_only_fields = ['guid']

class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = ['guid', 'price_list_name', 'price_list_code', 'is_inclusive_tax', 'is_active', 'is_default']
        read_only_fields = ['guid']

class POSCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSCounter
        fields = ['guid', 'counter_name', 'counter_code', 'branch', 
                 'godown', 'location', 'printer_name', 'receipt_header',
                 'receipt_footer', 'is_active']
        read_only_fields = ['guid']

class POSSessionSerializer(serializers.ModelSerializer):
    counter_name = serializers.CharField(source='counter.counter_name', read_only=True)
    opened_by_name = serializers.CharField(source='opened_by.get_full_name', read_only=True)
    
    class Meta:
        model = POSSession
        fields = ['guid', 'counter', 'counter_name', 'session_date', 
                 'opening_time', 'closing_time', 'opening_balance', 
                 'closing_balance', 'expected_cash', 'actual_cash',
                 'cash_difference', 'total_sales', 'total_returns',
                 'transaction_count', 'opened_by', 'opened_by_name',
                 'closed_by', 'status', 'notes']
        read_only_fields = ['guid', 'total_sales', 'total_returns', 
                          'transaction_count', 'cash_difference']

class ItemPriceSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    price_list_name = serializers.CharField(source='price_list.price_list_name', read_only=True)
    
    class Meta:
        model = ItemPrice
        fields = ['guid', 'item', 'item_name', 'price_list', 'price_list_name',
                 'mrp', 'selling_price', 'wholesale_price', 'discount_allowed',
                 'max_discount_percent']
        read_only_fields = ['guid']

class POSSaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSSaleItem
        fields = ['guid', 'item', 'item_name', 'barcode', 'hsn_code',
                 'quantity', 'uom', 'mrp', 'selling_price',
                 'discount_percent', 'discount_amount', 'taxable_amount',
                 'gst_rate', 'cgst_amount', 'sgst_amount', 'total_amount', 'line_total']
        read_only_fields = ['guid']

class POSSaleSerializer(serializers.ModelSerializer):
    items = POSSaleItemSerializer(many=True, required=False)
    counter_name = serializers.CharField(source='counter.counter_name', read_only=True)
    
    class Meta:
        model = POSSale
        fields = ['guid', 'invoice_no', 'counter', 'counter_name', 
                 'session', 'customer', 'invoice_date', 'subtotal',
                 'discount_amount', 'taxable_amount', 'cgst_amount', 'sgst_amount',
                 'grand_total', 'payment_method', 'items', 'created_at']
        read_only_fields = ['guid', 'subtotal', 
                           'discount_amount', 'taxable_amount', 'cgst_amount', 
                           'sgst_amount', 'grand_total', 'created_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        validated_data['guid'] = str(uuid.uuid4())
        sale = POSSale.objects.create(**validated_data)
        
        for item_data in items_data:
            item_data['guid'] = str(uuid.uuid4())
            item_data['sale'] = sale
            POSSaleItem.objects.create(**item_data)
        
        return sale

class POSPaymentSerializer(serializers.ModelSerializer):
    sale_invoice = serializers.CharField(source='sale.invoice_no', read_only=True)
    
    class Meta:
        model = POSPayment
        fields = ['guid', 'sale', 'sale_invoice', 'payment_method',
                 'amount', 'reference_number', 'transaction_id', 'status']
        read_only_fields = ['guid']
