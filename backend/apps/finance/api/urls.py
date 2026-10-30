from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .report_views import TrialBalanceView, ProfitLossView, BalanceSheetView
from .views import (AccountGroupViewSet, LedgerViewSet, VoucherViewSet,
                    VoucherTypeViewSet, AccountingEntryViewSet)

router = DefaultRouter()
router.register(r'voucher-types', VoucherTypeViewSet)
router.register(r'account-groups', AccountGroupViewSet)
router.register(r'ledgers', LedgerViewSet)
router.register(r'vouchers', VoucherViewSet)
router.register(r'accounting-entries', AccountingEntryViewSet)

urlpatterns = [
    path('reports/trial-balance/', TrialBalanceView.as_view(), name='report-trial-balance'),
    path('reports/profit-loss/', ProfitLossView.as_view(), name='report-profit-loss'),
    path('reports/balance-sheet/', BalanceSheetView.as_view(), name='report-balance-sheet'),
    path('', include(router.urls)),
]
