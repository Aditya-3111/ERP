from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.crm.models import Customer, Lead, Quotation, PurchaseInquiry, PurchaseOrder
from .serializers import (CustomerSerializer, LeadSerializer, 
                             QuotationSerializer, InquirySerializer,
                             PurchaseOrderSerializer)
from rest_framework.permissions import IsAuthenticated

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'company', 'contact_person', 'email', 'gstin']
    filterset_fields = ['customer_type', 'status', 'city', 'state']
    ordering_fields = ['name', 'credit_limit', 'created_at']
    ordering = ['name']

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['contact_person', 'company', 'email', 'mobile']
    filterset_fields = ['status', 'source', 'priority']
    ordering_fields = ['created_at', 'company']
    ordering = ['-created_at']

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseInquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['supplier_name', 'item_required']
    filterset_fields = ['status', 'priority', 'expected_date']
    ordering_fields = ['date', 'expected_date']
    ordering = ['-date']

class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['quote_no', 'customer_name']
    filterset_fields = ['status', 'date', 'customer_name']
    ordering_fields = ['date', 'total', 'created_at']
    ordering = ['-created_at']

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['po_no', 'supplier_name']
    filterset_fields = ['status', 'date', 'supplier_name']
    ordering_fields = ['date', 'total', 'created_at']
    ordering = ['-created_at']
