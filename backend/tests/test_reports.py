"""Trial balance, profit & loss, balance sheet and the dashboard."""
from datetime import date

from django.core.management import call_command

from tests.base import BaseAPITest


class ReportTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        call_command('seed_masters', verbosity=0)
        self.post_voucher('Sales', [('Cash', 1180, True), ('Sales Account', 1000, False), ('Output GST', 180, False)])
        self.post_voucher('Purchase', [('Purchase Account', 400, True), ('Input GST', 72, True), ('Cash', 472, False)])
        self.post_voucher('Payment', [('Cash', 100, False)] + [('Purchase Account', 100, True)])

    def post_voucher(self, vtype, lines):
        r = self.client.post('/api/finance/vouchers/', {
            'date': '2026-05-10', 'voucher_type': vtype, 'party_name': 'Test',
            'items': [{'ledger': l, 'amount': a, 'is_dr': d} for l, a, d in lines]}, format='json')
        self.assertEqual(r.status_code, 201, r.content)

    def get(self, name, query='?from=2026-04-01&to=2026-12-31'):
        r = self.client.get(f'/api/finance/reports/{name}/{query}')
        self.assertEqual(r.status_code, 200, r.content)
        return r.json()

    def test_trial_balance_balances(self):
        tb = self.get('trial-balance')
        self.assertTrue(tb['is_balanced'])
        self.assertAlmostEqual(tb['totals']['debit'], tb['totals']['credit'])
        cash = next(r for r in tb['rows'] if r['ledger'] == 'Cash')
        self.assertEqual((cash['debit'], cash['credit']), (1180.0, 572.0))
        self.assertEqual(cash['closing_dr'], 608.0)

    def test_opening_balance_uses_earlier_entries(self):
        tb = self.get('trial-balance', '?from=2026-06-01&to=2026-12-31')   # voucher is before 'from'
        cash = next(r for r in tb['rows'] if r['ledger'] == 'Cash')
        self.assertEqual(cash['opening_dr'], 608.0)
        self.assertEqual(cash['debit'], 0.0)

    def test_profit_and_loss(self):
        pl = self.get('profit-loss')
        self.assertEqual(pl['trading']['total_income'], 1000.0)      # sales
        self.assertEqual(pl['trading']['total_expense'], 500.0)      # purchases 400 + 100
        self.assertEqual(pl['gross_profit'], 500.0)
        self.assertEqual(pl['net_profit'], 500.0)

    def test_balance_sheet_balances_and_includes_profit(self):
        bs = self.get('balance-sheet')
        self.assertEqual(bs['difference'], 0.0)
        self.assertTrue(any(g['group'] == 'Profit & Loss A/c' for g in bs['liabilities']))

    def test_cancelled_vouchers_are_ignored(self):
        before = self.get('trial-balance')['totals']['debit']          # 1180 + 472 + 400 + 72 + 100 ...
        v = self.client.get('/api/finance/vouchers/?search=Test').json()['results'][0]
        self.client.patch(f"/api/finance/vouchers/{v['guid']}/", {'status': 'cancelled'}, format='json')
        after = self.get('trial-balance')['totals']['debit']
        self.assertLess(after, before)

    def test_dashboard_numbers(self):
        d = self.client.get('/api/core/dashboard/?from=2026-04-01&to=2026-12-31').json()
        self.assertEqual(d['finance']['sales'], 1000.0)
        self.assertEqual(d['finance']['purchase'], 500.0)
        self.assertEqual(d['counts']['vouchers'], 3)
        self.assertEqual(len(d['monthly']), 6)
        self.assertEqual(d['recent_vouchers'][0]['voucher_type'] in ('Sales', 'Purchase', 'Payment'), True)

    def test_dashboard_chart_never_shows_future_months(self):
        from django.utils import timezone
        d = self.client.get('/api/core/dashboard/?from=2026-04-01&to=2099-03-31').json()
        last = d['monthly'][-1]['month']
        self.assertEqual(last, timezone.localdate().strftime('%b %Y'))
