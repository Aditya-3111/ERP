from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (WorkCenterViewSet, MachineViewSet, OperationViewSet,
                       BOMHeaderViewSet, BOMItemViewSet,
                       ProductionOrderViewSet, ProductionOutputViewSet,
                       QualityInspectionViewSet)

router = DefaultRouter()
router.register(r'work-centers', WorkCenterViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'operations', OperationViewSet)
router.register(r'bom-headers', BOMHeaderViewSet)
router.register(r'bom-items', BOMItemViewSet)
router.register(r'orders', ProductionOrderViewSet)
router.register(r'outputs', ProductionOutputViewSet)
router.register(r'quality-inspections', QualityInspectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
