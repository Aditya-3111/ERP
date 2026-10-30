from django.db import models
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.inventory.models import (UnitOfMeasure, StockGroup, StockCategory, 
                             Godown, StockItem, StockBatch, StockJournal, 
                             MaterialReceiptNote, MRNItem)
from .serializers import (UnitOfMeasureSerializer, StockGroupSerializer, 
                          StockCategorySerializer, GodownSerializer, 
                          StockItemSerializer, StockBatchSerializer, 
                          StockJournalSerializer, MaterialReceiptNoteSerializer)
from rest_framework.permissions import IsAuthenticated

class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'formal_name']
    ordering_fields = ['name']
    ordering = ['name']

class StockGroupViewSet(viewsets.ModelViewSet):
    queryset = StockGroup.objects.all()
    serializer_class = StockGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class StockCategoryViewSet(viewsets.ModelViewSet):
    queryset = StockCategory.objects.all()
    serializer_class = StockCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class GodownViewSet(viewsets.ModelViewSet):
    queryset = Godown.objects.all()
    serializer_class = GodownSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'city', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'gst_hsn_code']
    filterset_fields = ['category', 'uom', 'is_active']
    ordering_fields = ['name', 'closing_balance', 'closing_value']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def movements(self, request, pk=None):
        """GET /api/inventory/items/<guid>/movements/
        Receipts come from Material Receipt Notes (IN), issues from POS sales (OUT)."""
        from decimal import Decimal
        from apps.pos.models import POSSaleItem
        item = self.get_object()
        rows = []
        for r in MRNItem.objects.filter(item_name=item.name).select_related('mrn'):
            rows.append({'date': r.mrn.date, 'type': 'IN', 'reference': r.mrn.mrn_no,
                         'quantity_in': float(r.quantity), 'quantity_out': 0.0})
        for s in POSSaleItem.objects.filter(item=item).select_related('sale'):
            rows.append({'date': s.sale.invoice_date, 'type': 'OUT', 'reference': s.sale.invoice_no,
                         'quantity_in': 0.0, 'quantity_out': float(s.quantity)})
        rows.sort(key=lambda r: (str(r['date']), r['type']))
        bal = Decimal(item.opening_balance or 0)
        for r in rows:
            bal += Decimal(str(r['quantity_in'])) - Decimal(str(r['quantity_out']))
            r['balance'] = float(bal)
        return Response(rows)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        items = self.queryset.filter(
            closing_balance__lte=models.F('min_stock')
        )
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

class StockBatchViewSet(viewsets.ModelViewSet):
    queryset = StockBatch.objects.all()
    serializer_class = StockBatchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['batch_no', 'item__name']
    filterset_fields = ['item', 'godown']
    ordering_fields = ['exp_date', 'mfg_date']
    ordering = ['-exp_date']

class StockJournalViewSet(viewsets.ModelViewSet):
    queryset = StockJournal.objects.all()
    serializer_class = StockJournalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['item_name', 'reference']
    filterset_fields = ['item', 'date', 'type']
    ordering_fields = ['date']
    ordering = ['-date']

class MaterialReceiptNoteViewSet(viewsets.ModelViewSet):
    queryset = MaterialReceiptNote.objects.all()
    serializer_class = MaterialReceiptNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['mrn_no', 'supplier_name']
    filterset_fields = ['date', 'godown', 'status']
    ordering_fields = ['date', 'mrn_no']
    ordering = ['-date']
