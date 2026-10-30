from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UnitOfMeasureViewSet, StockGroupViewSet, StockCategoryViewSet,
                     GodownViewSet, StockItemViewSet, StockBatchViewSet,
                     StockJournalViewSet, MaterialReceiptNoteViewSet)

router = DefaultRouter()
router.register(r'units', UnitOfMeasureViewSet)
router.register(r'groups', StockGroupViewSet)
router.register(r'categories', StockCategoryViewSet)
router.register(r'godowns', GodownViewSet)
router.register(r'items', StockItemViewSet)
router.register(r'batches', StockBatchViewSet)
router.register(r'journals', StockJournalViewSet)
router.register(r'mrn', MaterialReceiptNoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
