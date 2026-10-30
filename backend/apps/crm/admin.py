from django.contrib import admin
from apps.crm.models import Customer, Lead, Activity, Quotation, QuotationItem, PurchaseInquiry, PurchaseOrder, PurchaseOrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'contact_person', 'mobile', 'gstin', 'status']
    list_filter = ['status', 'customer_type']
    search_fields = ['name', 'company', 'mobile', 'gstin']

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['company', 'contact_person', 'mobile', 'email', 'source', 'status']
    list_filter = ['status', 'source', 'priority']
    search_fields = ['company', 'contact_person', 'mobile', 'email']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['customer', 'activity_type', 'subject', 'date']
    list_filter = ['activity_type']
    search_fields = ['customer__name', 'subject']
    date_hierarchy = 'date'

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quote_no', 'date', 'customer_name', 'status', 'total']
    list_filter = ['status']
    search_fields = ['quote_no', 'customer_name']
    date_hierarchy = 'date'

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'item_name', 'qty', 'rate', 'amount']
    search_fields = ['item_name', 'quotation__quote_no']

@admin.register(PurchaseInquiry)
class PurchaseInquiryAdmin(admin.ModelAdmin):
    list_display = ['inquiry_no', 'date', 'supplier_name', 'item_required', 'status']
    list_filter = ['status']
    search_fields = ['inquiry_no', 'supplier_name']
    date_hierarchy = 'date'

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_no', 'date', 'supplier_name', 'status', 'total']
    list_filter = ['status']
    search_fields = ['po_no', 'supplier_name']
    date_hierarchy = 'date'

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['po', 'item_name', 'quantity', 'rate', 'amount']
    search_fields = ['item_name', 'po__po_no']
