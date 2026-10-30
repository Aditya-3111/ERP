from django.contrib import admin
from apps.pos.models import POSCounter, POSSession, PriceList, ItemPrice, POSCustomer, POSSale, POSSaleItem, PaymentMethod, POSPayment

@admin.register(POSCounter)
class POSCounterAdmin(admin.ModelAdmin):
    list_display = ['counter_name', 'counter_code', 'branch', 'godown', 'is_active']
    list_filter = ['is_active', 'branch']
    search_fields = ['counter_name', 'counter_code']

@admin.register(POSSession)
class POSSessionAdmin(admin.ModelAdmin):
    list_display = ['counter', 'session_date', 'opening_time', 'closing_time', 'status']
    list_filter = ['status']
    search_fields = ['counter__counter_name']
    date_hierarchy = 'session_date'

@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['price_list_name', 'price_list_code', 'is_inclusive_tax', 'is_active', 'is_default']
    list_filter = ['is_active', 'is_default', 'is_inclusive_tax']
    search_fields = ['price_list_name', 'price_list_code']

@admin.register(ItemPrice)
class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ['item', 'price_list', 'mrp', 'selling_price', 'wholesale_price']
    list_filter = ['price_list']
    search_fields = ['item__name']

@admin.register(POSCustomer)
class POSCustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'mobile', 'customer_type', 'loyalty_points']
    list_filter = ['customer_type']
    search_fields = ['customer_name', 'mobile']

@admin.register(POSSale)
class POSSaleAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'invoice_date', 'customer', 'grand_total', 'payment_method', 'status']
    list_filter = ['status', 'payment_method']
    search_fields = ['invoice_no', 'customer_name']
    date_hierarchy = 'invoice_date'

@admin.register(POSSaleItem)
class POSSaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'item_name', 'quantity', 'selling_price', 'total_amount']
    search_fields = ['item_name', 'sale__invoice_no']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['method_name', 'method_code', 'method_type', 'is_active']
    list_filter = ['is_active', 'method_type']
    search_fields = ['method_name', 'method_code']

@admin.register(POSPayment)
class POSPaymentAdmin(admin.ModelAdmin):
    list_display = ['sale', 'payment_method', 'amount', 'status']
    list_filter = ['status', 'payment_method']
    search_fields = ['sale__invoice_no']
