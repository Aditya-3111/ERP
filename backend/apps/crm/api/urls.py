from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomerViewSet, LeadViewSet,
                        QuotationViewSet, InquiryViewSet,
                        PurchaseOrderViewSet)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'inquiries', InquiryViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
