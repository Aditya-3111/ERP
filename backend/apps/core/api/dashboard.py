"""GET /api/core/dashboard/?from=YYYY-MM-DD&to=YYYY-MM-DD

One call that feeds the whole dashboard page, so the browser does not have to
download hundreds of rows just to show a few numbers.
"""
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count, F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def _date(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def _default_range():
    from apps.core.models import FinancialYear
    fy = FinancialYear.objects.filter(is_active=True).first()
    today = timezone.localdate()
    if fy:
        return fy.start_date, min(fy.end_date, today) if fy.start_date <= today else fy.end_date
    start = date(today.year if today.month >= 4 else today.year - 1, 4, 1)
    return start, today


def _month_starts(end, n):
    """The first day of each of the last n months, oldest first."""
    months, cur = [], end.replace(day=1)
    for _ in range(n):
        months.append(cur)
        cur = (cur - timedelta(days=1)).replace(day=1)
    return list(reversed(months))


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.crm.models import Customer, Lead
        from apps.finance import reports
        from apps.finance.models import AccountingEntry, Ledger, Voucher
        from apps.gate.models import Visitor
        from apps.hr.models import Attendance, Employee
        from apps.inventory.models import StockItem
        from apps.maintenance.models import WorkOrder

        d_from, d_to = _default_range()
        d_from = _date(request.query_params.get('from')) or d_from
        d_to = _date(request.query_params.get('to')) or d_to
        today = timezone.localdate()

        # ---- money figures (from the ledger balances)
        rows = reports.ledger_rows(d_from, d_to)
        sales = sum((r['credit'] - r['debit'] for r in rows if r['primary_group'] == 'Sales Accounts'), Decimal(0))
        purchase = sum((r['debit'] - r['credit'] for r in rows if r['primary_group'] == 'Purchase Accounts'), Decimal(0))
        cash_bank = sum((r['closing'] for r in rows if r['group'] in ('Bank Accounts', 'Cash-in-Hand')), Decimal(0))
        receivable = sum((r['closing'] for r in rows if r['group'] == 'Sundry Debtors'), Decimal(0))
        payable = sum((-r['closing'] for r in rows if r['group'] == 'Sundry Creditors'), Decimal(0))
        net_profit = reports.profit_loss(d_from, d_to)['net_profit']

        # ---- sales / purchase per month, last 6 months
        sales_names = [r['ledger'] for r in rows if r['primary_group'] == 'Sales Accounts']
        buy_names = [r['ledger'] for r in rows if r['primary_group'] == 'Purchase Accounts']
        months = _month_starts(min(d_to, today), 6)     # last 6 months, never future months
        chart_end = min(d_to, today)
        monthly = {m: {'month': m.strftime('%b %Y'), 'sales': 0.0, 'purchase': 0.0} for m in months}
        qs = (AccountingEntry.objects
              .filter(voucher__status='active', voucher__date__gte=months[0], voucher__date__lte=chart_end)
              .filter(ledger__in=sales_names + buy_names)
              .values('ledger', 'is_dr', year=ExtractYear('voucher__date'), month=ExtractMonth('voucher__date'))
              .annotate(total=Sum('amount')))
        for row in qs:
            key = date(row['year'], row['month'], 1)
            if key not in monthly:
                continue
            sign = -1 if row['is_dr'] else 1       # sales: Cr is positive
            if row['ledger'] in sales_names:
                monthly[key]['sales'] += sign * float(row['total'])
            else:
                monthly[key]['purchase'] += -sign * float(row['total'])

        # ---- other modules
        low_stock = StockItem.objects.filter(is_active=True, closing_balance__lte=F('min_stock'), min_stock__gt=0)
        att = defaultdict(int)
        for row in Attendance.objects.filter(date=today).values('status').annotate(n=Count('guid')):
            att[row['status']] = row['n']
        # list() first: MySQL cannot run  "WHERE id IN (SELECT ... LIMIT 6)"
        recent = list(Voucher.objects.order_by('-date', '-created_at')[:6])
        voucher_amount = {}
        for e in AccountingEntry.objects.filter(voucher__in=[v.pk for v in recent], is_dr=True).values('voucher').annotate(t=Sum('amount')):
            voucher_amount[e['voucher']] = float(e['t'])

        return Response({
            'range': {'from': d_from.isoformat(), 'to': d_to.isoformat()},
            'finance': {
                'sales': float(sales), 'purchase': float(purchase), 'net_profit': net_profit,
                'cash_bank': float(cash_bank), 'receivable': float(receivable), 'payable': float(payable),
            },
            'monthly': list(monthly.values()),
            'counts': {
                'ledgers': Ledger.objects.count(), 'vouchers': Voucher.objects.count(),
                'customers': Customer.objects.count(), 'leads': Lead.objects.count(),
                'open_leads': Lead.objects.exclude(status__in=['converted', 'lost']).count(),
                'stock_items': StockItem.objects.count(), 'low_stock': low_stock.count(),
                'employees': Employee.objects.filter(status='active').count(),
                'visitors_inside': Visitor.objects.filter(status='checked_in').count(),
                'open_work_orders': WorkOrder.objects.exclude(status__in=['completed', 'cancelled', 'closed']).count(),
            },
            'attendance_today': {
                'present': att['Present'], 'absent': att['Absent'],
                'half_day': att['Half Day'], 'leave': att['Leave'],
            },
            'recent_vouchers': [{
                'guid': str(v.guid), 'date': v.date.isoformat(), 'voucher_type': v.voucher_type,
                'voucher_number': v.voucher_number, 'party_name': v.party_name,
                'amount': voucher_amount.get(v.guid, 0.0),
            } for v in recent],
            'low_stock_items': [{
                'guid': str(i.guid), 'name': i.name, 'uom': i.uom,
                'closing_balance': float(i.closing_balance), 'min_stock': float(i.min_stock),
            } for i in low_stock.order_by('name')[:6]],
        })