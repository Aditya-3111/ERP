from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BreakdownViewSet, AssetCategoryViewSet, AssetViewSet,
                       MaintenanceScheduleViewSet, 
                       WorkOrderViewSet, 
                       WorkOrderTaskViewSet)

router = DefaultRouter()
router.register(r'categories', AssetCategoryViewSet)
# alias: the finledger HTML pages call /maintenance/asset-categories/
router.register(r'asset-categories', AssetCategoryViewSet, basename='asset-category-alias')
router.register(r'assets', AssetViewSet)
router.register(r'schedules', MaintenanceScheduleViewSet)
router.register(r'work-orders', WorkOrderViewSet)
router.register(r'tasks', WorkOrderTaskViewSet)
router.register(r'breakdowns', BreakdownViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
