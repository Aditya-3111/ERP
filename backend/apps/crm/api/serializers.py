from rest_framework import serializers
from apps.crm.models import Customer, Lead, Quotation, PurchaseInquiry, PurchaseOrder
import uuid

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['guid', 'name', 'company', 'customer_type', 'contact_person',
                 'designation', 'department', 'mobile', 'alt_mobile', 'email',
                 'website', 'source', 'industry', 'address_billing',
                 'address_shipping', 'city', 'state', 'pincode', 'country',
                 'gstin', 'pan', 'msme_no', 'credit_limit', 'credit_period',
                 'payment_terms', 'price_category', 'tax_registration_type',
                 'bank_name', 'bank_account', 'bank_ifsc', 'notes', 'status']
        read_only_fields = ['guid']

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['guid', 'company', 'contact_person', 'email', 'mobile', 'source',
                 'industry', 'status', 'priority', 'assigned_to', 'notes',
                 'follow_up_date', 'created_at']
        read_only_fields = ['guid', 'created_at']

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInquiry
        fields = ['guid', 'inquiry_no', 'date', 'supplier_name', 'contact_person',
                 'mobile', 'email', 'gstin', 'item_required', 'quantity', 'uom',
                 'expected_rate', 'expected_date', 'payment_terms', 'status',
                 'priority', 'remarks']
        read_only_fields = ['guid']

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['guid', 'quote_no', 'date', 'valid_upto', 'customer_name',
                 'customer_contact', 'customer_mobile', 'customer_email',
                 'customer_gstin', 'billing_address', 'shipping_address',
                 'reference', 'payment_terms', 'delivery_terms', 'delivery_time',
                 'freight', 'warranty', 'subtotal', 'cgst', 'sgst', 'igst',
                 'total', 'status', 'prepared_by', 'remarks', 'terms_conditions',
                 'created_at']
        read_only_fields = ['guid', 'created_at']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['guid', 'po_no', 'date', 'delivery_date', 'reference',
                 'supplier_name', 'contact_person', 'mobile', 'email', 'gstin',
                 'supplier_address', 'payment_terms', 'delivery_terms', 'freight',
                 'subtotal', 'cgst', 'sgst', 'total', 'status', 'remarks',
                 'created_at']
        read_only_fields = ['guid', 'created_at']
