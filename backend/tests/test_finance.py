"""Ledgers, vouchers, accounting entries."""
import uuid
from datetime import date

from tests.base import BaseAPITest


class FinanceTests(BaseAPITest):
    def test_ledger_keeps_gst_and_bank_details(self):
        r = self.client.post('/api/finance/ledgers/', {
            'name': 'Acme Traders', 'parent': 'Sundry Debtors',
            'gstin': '27ABCDE1234F1Z5', 'pan': 'ABCDE1234F',
            'bank_name': 'HDFC', 'bank_ifsc': 'HDFC0001234', 'opening_balance': 500,
        }, format='json')
        self.assertEqual(r.status_code, 201, r.content)
        got = self.client.get(f"/api/finance/ledgers/{r.json()['guid']}/").json()
        self.assertEqual(got['gstin'], '27ABCDE1234F1Z5')
        self.assertEqual(got['bank_ifsc'], 'HDFC0001234')

    def _voucher(self, **extra):
        body = {
            'date': str(date.today()), 'voucher_type': 'Sales', 'party_name': 'Acme',
            'items': [
                {'ledger': 'Acme', 'amount': '1180.00', 'is_dr': True},
                {'ledger': 'Sales A/c', 'amount': '1000.00', 'is_dr': False},
                {'ledger': 'GST Output', 'amount': '180.00', 'is_dr': False},
            ],
        }
        body.update(extra)
        return self.client.post('/api/finance/vouchers/', body, format='json')

    def test_voucher_returns_its_entries_and_auto_number(self):
        r = self._voucher()
        self.assertEqual(r.status_code, 201, r.content)
        vid = r.json()['guid']
        got = self.client.get(f'/api/finance/vouchers/{vid}/').json()
        self.assertEqual(len(got['items']), 3)          # used to be missing entirely
        self.assertTrue(got['voucher_number'])           # used to be blank
        self.assertEqual(self._voucher().json()['voucher_number'][-4:], '0002')

    def test_unbalanced_voucher_rejected(self):
        r = self._voucher(items=[
            {'ledger': 'A', 'amount': '100', 'is_dr': True},
            {'ledger': 'B', 'amount': '90', 'is_dr': False}])
        self.assertEqual(r.status_code, 400)

    def test_voucher_update_replaces_entries(self):
        vid = self._voucher().json()['guid']
        r = self.client.patch(f'/api/finance/vouchers/{vid}/', {'items': [
            {'ledger': 'Acme', 'amount': '50', 'is_dr': True},
            {'ledger': 'Sales A/c', 'amount': '50', 'is_dr': False}]}, format='json')
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(len(r.json()['items']), 2)

    def test_voucher_search_does_not_crash(self):          # used to be HTTP 500
        self._voucher()
        r = self.client.get('/api/finance/vouchers/?search=Acme')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['count'], 1)

    def test_accounting_entries_endpoint(self):
        vid = self._voucher(items=[]).json()['guid']
        r = self.client.post('/api/finance/accounting-entries/',
                             {'voucher': vid, 'ledger': 'Cash', 'amount': 10, 'is_dr': True}, format='json')
        self.assertEqual(r.status_code, 201, r.content)
        eid = r.json()['guid']
        self.assertEqual(len(self.client.get(f'/api/finance/vouchers/{vid}/').json()['items']), 1)
        self.assertEqual(self.client.delete(f'/api/finance/accounting-entries/{eid}/').status_code, 204)


class VoucherDateRangeTests(BaseAPITest):
    def test_from_to_filter(self):
        for d in ('2026-04-10', '2026-06-10', '2026-09-10'):
            self.client.post('/api/finance/vouchers/', {'date': d, 'voucher_type': 'Journal'}, format='json')
        got = self.client.get('/api/finance/vouchers/?from=2026-05-01&to=2026-07-01').json()
        self.assertEqual(got['count'], 1)
        # a badly written date is ignored, not a crash
        self.assertEqual(self.client.get('/api/finance/vouchers/?from=nonsense').status_code, 200)


class UniqueNameTests(BaseAPITest):
    def test_ledger_group_and_voucher_type_names_are_unique(self):
        for url, body in (('/api/finance/ledgers/', {'name': 'Cash', 'parent': 'Cash-in-Hand'}),
                          ('/api/finance/account-groups/', {'name': 'Grp'}),
                          ('/api/finance/voucher-types/', {'name': 'Special'})):
            self.assertEqual(self.client.post(url, body, format='json').status_code, 201, url)
            dup = self.client.post(url, body, format='json')
            self.assertEqual(dup.status_code, 400, url)
            self.assertIn('already exists', str(dup.json()))
