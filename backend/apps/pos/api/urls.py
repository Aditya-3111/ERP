from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PaymentMethodViewSet, PriceListViewSet,
                        POSCounterViewSet, POSSessionViewSet, 
                        ItemPriceViewSet, POSSaleViewSet, 
                        POSPaymentViewSet)

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'price-lists', PriceListViewSet)
router.register(r'counters', POSCounterViewSet)
router.register(r'sessions', POSSessionViewSet)
router.register(r'prices', ItemPriceViewSet)
router.register(r'sales', POSSaleViewSet)
router.register(r'payments', POSPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
