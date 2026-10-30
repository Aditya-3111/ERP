from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.finance import reports


def _parse(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


class _ReportView(APIView):
    """GET ...?from=YYYY-MM-DD&to=YYYY-MM-DD   (both optional)."""
    permission_classes = [IsAuthenticated]
    builder = None

    def get(self, request):
        date_from = _parse(request.query_params.get('from'))
        date_to = _parse(request.query_params.get('to'))
        data = type(self).builder(date_from, date_to)
        data['from'] = date_from.isoformat() if date_from else None
        data['to'] = date_to.isoformat() if date_to else None
        return Response(data)


class TrialBalanceView(_ReportView):
    builder = staticmethod(reports.trial_balance)


class ProfitLossView(_ReportView):
    builder = staticmethod(reports.profit_loss)


class BalanceSheetView(_ReportView):
    builder = staticmethod(reports.balance_sheet)
