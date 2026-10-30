from django.contrib import admin
from apps.inventory.models import UnitOfMeasure, StockGroup, StockCategory, Godown, StockItem, StockJournal, StockBatch, MaterialReceiptNote

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'formal_name', 'is_simple_unit', 'base_units', 'conversion']
    list_filter = ['is_simple_unit']
    search_fields = ['name', 'formal_name']

@admin.register(StockGroup)
class StockGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']

@admin.register(StockCategory)
class StockCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']

@admin.register(Godown)
class GodownAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'city', 'state', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'city']

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'part_number', 'uom', 'opening_balance', 'min_stock', 'is_active']
    list_filter = ['is_active', 'costing_method']
    search_fields = ['name', 'part_number', 'category']
    list_editable = ['min_stock']

@admin.register(StockJournal)
class StockJournalAdmin(admin.ModelAdmin):
    list_display = ['date', 'item', 'quantity', 'godown', 'destination_godown', 'reference']
    search_fields = ['item', 'reference']
    date_hierarchy = 'date'

@admin.register(StockBatch)
class StockBatchAdmin(admin.ModelAdmin):
    list_display = ['item', 'batch_no', 'mfg_date', 'exp_date', 'quantity']
    search_fields = ['batch_no', 'item']
    list_filter = ['item']

@admin.register(MaterialReceiptNote)
class MaterialReceiptNoteAdmin(admin.ModelAdmin):
    list_display = ['mrn_no', 'date', 'supplier_name', 'godown', 'status']
    list_filter = ['status']
    search_fields = ['mrn_no', 'supplier_name']
    date_hierarchy = 'date'
