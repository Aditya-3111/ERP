from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.production.models import (WorkCenter, Machine, Operation, 
                              BOMHeader, BOMItem, 
                              ProductionOrder, ProductionOutput, 
                              QualityInspection)
from .serializers import (WorkCenterSerializer, MachineSerializer, 
                          OperationSerializer, BOMHeaderSerializer, 
                          BOMItemSerializer, ProductionOrderSerializer, 
                          ProductionOutputSerializer, 
                          QualityInspectionSerializer)
from rest_framework.permissions import IsAuthenticated

class WorkCenterViewSet(viewsets.ModelViewSet):
    queryset = WorkCenter.objects.all()
    serializer_class = WorkCenterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['work_center_name', 'department', 'location']
    filterset_fields = ['is_active']
    ordering_fields = ['work_center_name', 'cost_per_hour']
    ordering = ['work_center_name']

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['machine_name', 'machine_type']
    filterset_fields = ['work_center', 'is_active']
    ordering_fields = ['machine_name', 'capacity_per_hour']
    ordering = ['machine_name']

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['operation_name']
    filterset_fields = ['work_center', 'is_active']
    ordering_fields = ['operation_name', 'setup_time_minutes']
    ordering = ['operation_name']

class BOMHeaderViewSet(viewsets.ModelViewSet):
    queryset = BOMHeader.objects.all()
    serializer_class = BOMHeaderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['bom_name', 'finished_item__name']
    filterset_fields = ['finished_item', 'is_active', 'bom_type']
    ordering_fields = ['bom_name']
    ordering = ['bom_name']

class BOMItemViewSet(viewsets.ModelViewSet):
    queryset = BOMItem.objects.all()
    serializer_class = BOMItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['bom__bom_name', 'item__name']
    filterset_fields = ['bom', 'item']
    ordering_fields = ['item__name', 'required_quantity']
    ordering = ['item__name']

class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['order_no', 'finished_item__name']
    filterset_fields = ['status', 'priority']
    ordering_fields = ['order_no', 'planned_start_date', 'planned_quantity']
    ordering = ['-planned_start_date']

class ProductionOutputViewSet(viewsets.ModelViewSet):
    queryset = ProductionOutput.objects.all()
    serializer_class = ProductionOutputSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['order__order_no', 'item__name']
    filterset_fields = ['order', 'status']
    ordering_fields = ['output_date']
    ordering = ['-output_date']

class QualityInspectionViewSet(viewsets.ModelViewSet):
    queryset = QualityInspection.objects.all()
    serializer_class = QualityInspectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['order__order_no', 'item__name']
    filterset_fields = ['order', 'inspection_date', 'inspection_result']
    ordering_fields = ['inspection_date']
    ordering = ['-inspection_date']
