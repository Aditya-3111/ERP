from django.contrib import admin
from apps.finance.models import AccountGroup, Ledger, VoucherType, Voucher, AccountingEntry, InventoryEntry

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_revenue', 'is_deemed_positive', 'affects_gross_profit']
    list_filter = ['is_revenue', 'is_deemed_positive', 'affects_gross_profit']
    search_fields = ['name']

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'opening_balance', 'opening_balance_type']
    search_fields = ['name']
    list_filter = ['opening_balance_type']

@admin.register(VoucherType)
class VoucherTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'numbering_method', 'is_deemed_positive', 'affects_stock']
    search_fields = ['name']
    list_filter = ['affects_stock']

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['voucher_number', 'voucher_type', 'date', 'party_name', 'status']
    list_filter = ['voucher_type', 'status']
    search_fields = ['voucher_number', 'party_name']
    date_hierarchy = 'date'

@admin.register(AccountingEntry)
class AccountingEntryAdmin(admin.ModelAdmin):
    list_display = ['voucher', 'ledger', 'amount']
    search_fields = ['ledger', 'voucher__voucher_number']

@admin.register(InventoryEntry)
class InventoryEntryAdmin(admin.ModelAdmin):
    list_display = ['voucher', 'item', 'quantity', 'rate', 'amount']
    search_fields = ['item', 'voucher__voucher_number']
