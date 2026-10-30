"""python manage.py seed_masters

The data every FinLedger installation needs: roles, financial years, company
profile, head-office branch, Tally-style account groups, voucher types, units of
measure, default ledgers and the first admin login.  Idempotent.
"""
from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import Branch, CompanyProfile, FinancialYear, Role, User
from apps.finance.models import AccountGroup, Ledger, VoucherType
from apps.inventory.models import UnitOfMeasure

# name, label
ROLES = [
    ('admin', 'Administrator'), ('accountant', 'Accountant'), ('sales', 'Sales'),
    ('store', 'Store Keeper'), ('hr', 'HR Manager'), ('gate', 'Gate Security'),
    ('production', 'Production'), ('maintenance', 'Maintenance'),
]

# (name, parent, is_primary, is_revenue, is_deemed_positive, affects_gross_profit)
#   is_deemed_positive = the group normally has a DEBIT balance (assets, expenses)
GROUPS = [
    ('Capital Account', '', True, False, False, False),
    ('Reserves & Surplus', 'Capital Account', False, False, False, False),
    ('Current Assets', '', True, False, True, False),
    ('Bank Accounts', 'Current Assets', False, False, True, False),
    ('Cash-in-Hand', 'Current Assets', False, False, True, False),
    ('Deposits (Asset)', 'Current Assets', False, False, True, False),
    ('Loans & Advances (Asset)', 'Current Assets', False, False, True, False),
    ('Stock-in-Hand', 'Current Assets', False, False, True, False),
    ('Sundry Debtors', 'Current Assets', False, False, True, False),
    ('Current Liabilities', '', True, False, False, False),
    ('Duties & Taxes', 'Current Liabilities', False, False, False, False),
    ('Provisions', 'Current Liabilities', False, False, False, False),
    ('Sundry Creditors', 'Current Liabilities', False, False, False, False),
    ('Fixed Assets', '', True, False, True, False),
    ('Investments', '', True, False, True, False),
    ('Loans (Liability)', '', True, False, False, False),
    ('Bank OD A/c', 'Loans (Liability)', False, False, False, False),
    ('Secured Loans', 'Loans (Liability)', False, False, False, False),
    ('Unsecured Loans', 'Loans (Liability)', False, False, False, False),
    ('Misc. Expenses (ASSET)', '', True, False, True, False),
    ('Suspense A/c', '', True, False, False, False),
    ('Sales Accounts', '', True, True, False, True),
    ('Purchase Accounts', '', True, True, True, True),
    ('Direct Incomes', '', True, True, False, True),
    ('Direct Expenses', '', True, True, True, True),
    ('Indirect Incomes', '', True, True, False, False),
    ('Indirect Expenses', '', True, True, True, False),
]

# (name, parent)
VOUCHER_TYPES = [
    ('Sales', ''), ('Purchase', ''), ('Receipt', ''), ('Payment', ''), ('Journal', ''),
    ('Contra', ''), ('Credit Note', ''), ('Debit Note', ''),
]

# (name, group, opening_balance, 'dr'/'cr')
LEDGERS = [
    ('Cash', 'Cash-in-Hand', 0, 'dr'),
    ('Sales Account', 'Sales Accounts', 0, 'dr'),
    ('Purchase Account', 'Purchase Accounts', 0, 'dr'),
    ('Output GST', 'Duties & Taxes', 0, 'cr'),
    ('Input GST', 'Duties & Taxes', 0, 'dr'),
]

UNITS = [('Nos', 'Numbers'), ('Pcs', 'Pieces'), ('Kg', 'Kilogram'), ('Ltr', 'Litre'),
         ('Mtr', 'Metre'), ('Box', 'Box'), ('Set', 'Set')]


class Command(BaseCommand):
    help = 'Create roles, groups, voucher types, financial years and the admin user (idempotent).'

    def log(self, opts, text):
        if opts.get('verbosity', 1) > 0:
            self.stdout.write(text)

    def handle(self, *args, **opts):
        roles = {}
        for name, label in ROLES:
            roles[name], _ = Role.objects.get_or_create(
                name=name, defaults={'label': label, 'is_system': True,
                                     'description': f'{label} role'})

        today = timezone.localdate()
        start_year = today.year if today.month >= 4 else today.year - 1
        for y in (start_year - 1, start_year):
            FinancialYear.objects.get_or_create(
                name=f'FY {y}-{str(y + 1)[2:]}',
                defaults={'start_date': date(y, 4, 1), 'end_date': date(y + 1, 3, 31),
                          'is_active': y == start_year})

        CompanyProfile.objects.get_or_create(
            company_name='FinLedger Demo Company',
            defaults={'legal_name': 'FinLedger Demo Company Pvt Ltd', 'city': 'Mumbai',
                      'state': 'Maharashtra', 'country': 'India', 'address': '123 Business Park, Mumbai',
                      'gstin': '27AABCF1234A1Z5', 'pan': 'AABCF1234A', 'email': 'info@finledger.local'})
        Branch.objects.get_or_create(name='Head Office', defaults={'code': 'HO', 'city': 'Mumbai',
                                                                  'state': 'Maharashtra'})

        for i, (name, parent, primary, revenue, positive, gp) in enumerate(GROUPS):
            AccountGroup.objects.get_or_create(
                name=name,
                defaults={'parent': parent, 'primary_group': name if primary else '',
                          'is_revenue': revenue, 'is_deemed_positive': positive,
                          'affects_gross_profit': gp, 'is_reserved': True, 'sort_position': i})
        # sub-groups know their primary group (used by the reports)
        by_name = {g[0]: g for g in GROUPS}
        for name, parent, primary, *_ in GROUPS:
            if not primary:
                AccountGroup.objects.filter(name=name).update(primary_group=parent)

        for name, parent in VOUCHER_TYPES:
            VoucherType.objects.get_or_create(
                name=name, defaults={'parent': parent, 'numbering_method': 'Automatic'})

        for name, formal in UNITS:
            UnitOfMeasure.objects.get_or_create(name=name, defaults={'formal_name': formal})

        for name, group, opening, typ in LEDGERS:
            positive = by_name[group][4] if group in by_name else True
            Ledger.objects.get_or_create(
                name=name, defaults={'parent': group, 'opening_balance': opening,
                                     'opening_balance_type': typ, 'is_deemed_positive': positive})

        if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
            User.objects.create_superuser(
                username=settings.ADMIN_USERNAME, email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD, role=roles['admin'],
                first_name='System', last_name='Admin')
            self.log(opts, f'Created admin user "{settings.ADMIN_USERNAME}"')
        self.log(opts, self.style.SUCCESS('Masters ready.'))
