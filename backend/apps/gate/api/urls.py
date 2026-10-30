from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (VisitorViewSet, TransporterViewSet, GateEntryViewSet,
                       VisitorLogViewSet)

router = DefaultRouter()
router.register(r'visitors', VisitorViewSet)
router.register(r'transporters', TransporterViewSet)
router.register(r'entries', GateEntryViewSet)
router.register(r'logs', VisitorLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
