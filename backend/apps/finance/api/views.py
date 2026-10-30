from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from datetime import date
from decimal import Decimal
from apps.finance.models import AccountGroup, Ledger, Voucher, AccountingEntry, VoucherType
from .serializers import (AccountGroupSerializer, LedgerSerializer, VoucherSerializer,
                          VoucherTypeSerializer, AccountingEntrySerializer)


class VoucherTypeViewSet(viewsets.ModelViewSet):
    queryset = VoucherType.objects.all()
    serializer_class = VoucherTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'parent']
    ordering_fields = ['name']
    ordering = ['name']


class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'primary_group']
    ordering_fields = ['name', 'sort_position']
    ordering = ['sort_position', 'name']

    def perform_create(self, serializer):
        serializer.save()


class LedgerViewSet(viewsets.ModelViewSet):
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'mailing_name', 'city', 'contact_person', 'gstin']
    filterset_fields = ['is_revenue', 'is_deemed_positive', 'opening_balance_type', 'parent', 'is_active']
    ordering_fields = ['name', 'opening_balance']
    ordering = ['name']

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        ledger = self.get_object()
        rows = self._statement(ledger)
        response.data['current_balance'] = rows[-1]['balance'] if rows else float(ledger.opening_balance)
        return response

    @staticmethod
    def _statement(ledger):
        """Running statement. Balance is positive for Dr, negative for Cr."""
        opening = Decimal(ledger.opening_balance or 0)
        balance = opening if (ledger.opening_balance_type or 'dr').lower().startswith('d') else -opening
        entries = (AccountingEntry.objects.filter(ledger=ledger.name)
                   .select_related('voucher').order_by('voucher__date', 'voucher__created_at'))
        rows = []
        for e in entries:
            amt = Decimal(e.amount)
            balance += amt if e.is_dr else -amt
            rows.append({
                'date': e.voucher.date, 'voucher_number': e.voucher.voucher_number,
                'voucher_type': e.voucher.voucher_type,
                'particulars': e.narration or e.voucher.party_name or e.voucher.narration,
                'debit': float(amt) if e.is_dr else 0.0,
                'credit': 0.0 if e.is_dr else float(amt),
                'balance': float(balance),
            })
        return rows

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """GET /api/finance/ledgers/<guid>/transactions/ - ledger statement."""
        return Response(self._statement(self.get_object()))

    @action(detail=False, methods=['get'])
    def by_group(self, request):
        group_id = request.query_params.get('group_id')
        if group_id:
            ledgers = self.queryset.filter(parent=group_id)
            serializer = self.get_serializer(ledgers, many=True)
            return Response(serializer.data)
        return Response({'error': 'group_id required'}, status=400)


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.prefetch_related('accounting_entries').all()
    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # 'reference' used to be listed here but no such field exists -> ?search= returned HTTP 500
    search_fields = ['voucher_number', 'narration', 'reference_number', 'party_name']
    filterset_fields = ['voucher_type', 'date', 'status']
    ordering_fields = ['date', 'voucher_number']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        """Optional date range:  /vouchers/?from=2026-04-01&to=2027-03-31"""
        qs = super().get_queryset()
        for param, lookup in (('from', 'date__gte'), ('to', 'date__lte')):
            value = self.request.query_params.get(param)
            if value:
                try:
                    qs = qs.filter(**{lookup: date.fromisoformat(value)})
                except ValueError:
                    pass          # ignore a badly written date instead of crashing
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AccountingEntryViewSet(viewsets.ModelViewSet):
    """Used by jsfrontend (api.js -> createEntries / deleteEntries)."""
    queryset = AccountingEntry.objects.all()
    serializer_class = AccountingEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['ledger', 'narration']
    filterset_fields = ['voucher', 'ledger', 'is_dr']
    ordering = ['voucher', 'guid']
