from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.gate.models import Visitor, Transporter, GateEntry, VisitorLog
from .serializers import (VisitorSerializer, TransporterSerializer, 
                           GateEntrySerializer, VisitorLogSerializer)
from rest_framework.permissions import IsAuthenticated

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'company', 'mobile', 'email']
    filterset_fields = ['entry_date', 'status']
    ordering_fields = ['entry_date', 'entry_time', 'name']
    ordering = ['-entry_date', '-entry_time']

class TransporterViewSet(viewsets.ModelViewSet):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'contact']
    filterset_fields = ['is_active']
    ordering_fields = ['name']
    ordering = ['name']

class GateEntryViewSet(viewsets.ModelViewSet):
    queryset = GateEntry.objects.all()
    serializer_class = GateEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['party_name', 'vehicle_no', 'challan_no']
    filterset_fields = ['type', 'date', 'status', 'transporter']
    ordering_fields = ['date', 'time']
    ordering = ['-date', '-time']
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        entries = self.queryset.filter(status='PENDING')
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)

class VisitorLogViewSet(viewsets.ModelViewSet):
    queryset = VisitorLog.objects.all()
    serializer_class = VisitorLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['visitor__name', 'details']
    filterset_fields = ['visitor', 'action']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
