from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.maintenance.models import (Breakdown, AssetCategory, Asset, MaintenanceSchedule,
                                 WorkOrder, WorkOrderTask)
from .serializers import (BreakdownSerializer, AssetCategorySerializer, AssetSerializer,
                          MaintenanceScheduleSerializer, 
                          WorkOrderSerializer, 
                          WorkOrderTaskSerializer)
from rest_framework.permissions import IsAuthenticated

class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['category_name', 'category_code']
    filterset_fields = ['is_active', 'parent']
    ordering_fields = ['category_name', 'depreciation_rate']
    ordering = ['category_name']

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['asset_name', 'asset_code', 'manufacturer', 'serial_no']
    filterset_fields = ['category', 'asset_type', 'status', 'criticality', 
                       'department']
    ordering_fields = ['asset_name', 'purchase_date', 'current_value']
    ordering = ['asset_name']
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        assets = self.queryset.filter(criticality='critical')
        serializer = self.get_serializer(assets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def under_maintenance(self, request):
        assets = self.queryset.filter(status='under_maintenance')
        serializer = self.get_serializer(assets, many=True)
        return Response(serializer.data)

class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['asset__asset_name']
    filterset_fields = ['asset', 'schedule_name', 'frequency_type', 'priority', 'status']
    ordering_fields = ['next_due_date', 'start_date']
    ordering = ['next_due_date']
    
    @action(detail=False, methods=['get'])
    def due_soon(self, request):
        from django.utils import timezone
        from datetime import timedelta
        due_date = timezone.now().date() + timedelta(days=7)
        schedules = self.queryset.filter(next_due_date__lte=due_date, status='active')
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['wo_no', 'asset__asset_name', 'problem_description']
    filterset_fields = ['asset', 'wo_type', 'status', 'priority', 'assigned_technician']
    ordering_fields = ['wo_date', 'planned_start', 'actual_end', 'actual_cost']
    ordering = ['-wo_date']
    
    @action(detail=False, methods=['get'])
    def open_orders(self, request):
        orders = self.queryset.exclude(status__in=['completed', 'cancelled'])
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class WorkOrderTaskViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderTask.objects.all()
    serializer_class = WorkOrderTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['work_order__wo_no', 'task_description']
    filterset_fields = ['work_order', 'is_completed']
    ordering_fields = ['sequence_no', 'completed_at']
    ordering = ['sequence_no']


class BreakdownViewSet(viewsets.ModelViewSet):
    queryset = Breakdown.objects.select_related('asset').all()
    serializer_class = BreakdownSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['breakdown_no', 'problem_description', 'asset__name']
    filterset_fields = ['asset', 'status', 'severity', 'breakdown_type']
    ordering_fields = ['breakdown_date', 'status']
    ordering = ['-breakdown_date']
