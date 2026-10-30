from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.pos.models import (POSCounter, POSSession, ItemPrice, POSSale, 
                          POSPayment, PaymentMethod, PriceList)
from .serializers import (PaymentMethodSerializer, PriceListSerializer,
                           POSCounterSerializer, POSSessionSerializer,
                           ItemPriceSerializer, POSSaleSerializer,
                           POSPaymentSerializer)
from rest_framework.permissions import IsAuthenticated

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['method_name', 'method_code']
    filterset_fields = ['method_type', 'is_active']
    ordering_fields = ['method_name']
    ordering = ['method_name']

class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['price_list_name', 'price_list_code']
    filterset_fields = ['is_active', 'is_default']
    ordering_fields = ['price_list_name']
    ordering = ['price_list_name']

class POSCounterViewSet(viewsets.ModelViewSet):
    queryset = POSCounter.objects.all()
    serializer_class = POSCounterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['counter_name', 'counter_code', 'location']
    filterset_fields = ['branch', 'godown', 'is_active']
    ordering_fields = ['counter_name', 'counter_code']
    ordering = ['counter_name']

class POSSessionViewSet(viewsets.ModelViewSet):
    queryset = POSSession.objects.all()
    serializer_class = POSSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['counter__counter_name']
    filterset_fields = ['counter', 'session_date', 'status', 'opened_by']
    ordering_fields = ['session_date', 'opening_time', 'total_sales']
    ordering = ['-session_date', '-opening_time']
    
    @action(detail=False, methods=['get'])
    def open_sessions(self, request):
        sessions = self.queryset.filter(status='open')
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

class ItemPriceViewSet(viewsets.ModelViewSet):
    queryset = ItemPrice.objects.all()
    serializer_class = ItemPriceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['item__name', 'price_list__price_list_name']
    filterset_fields = ['item', 'price_list']
    ordering_fields = ['item', 'selling_price']
    ordering = ['selling_price']

class POSSaleViewSet(viewsets.ModelViewSet):
    queryset = POSSale.objects.all()
    serializer_class = POSSaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['invoice_no', 'customer_name']
    filterset_fields = ['counter', 'session', 'customer', 'invoice_date', 'payment_method']
    ordering_fields = ['invoice_date', 'invoice_no', 'grand_total']
    ordering = ['-invoice_date', '-invoice_no']
    
    def perform_create(self, serializer):
        serializer.save()

class POSPaymentViewSet(viewsets.ModelViewSet):
    queryset = POSPayment.objects.all()
    serializer_class = POSPaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['sale__invoice_no', 'reference_number', 'transaction_id']
    filterset_fields = ['sale', 'payment_method', 'status']
    ordering_fields = ['amount']
    ordering = ['-amount']
