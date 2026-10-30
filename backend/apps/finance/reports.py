"""Accounting reports computed from ledgers + voucher entries.

All three reports use one building block, :func:`ledger_rows`, which gives the
opening / period / closing figure of every ledger.

Sign convention used inside this file:  Dr balance = positive,  Cr balance = negative.
"""
from collections import defaultdict
from decimal import Decimal

from django.db.models import Q, Sum

from .models import AccountGroup, AccountingEntry, Ledger

ZERO = Decimal('0')

# Tally's reserved primary groups -> what kind of account they hold.
PRIMARY_NATURE = {
    'Current Assets': 'asset', 'Fixed Assets': 'asset', 'Investments': 'asset',
    'Misc. Expenses (ASSET)': 'asset',
    'Capital Account': 'liability', 'Current Liabilities': 'liability',
    'Loans (Liability)': 'liability', 'Suspense A/c': 'liability',
    'Sales Accounts': 'income', 'Direct Incomes': 'income', 'Indirect Incomes': 'income',
    'Purchase Accounts': 'expense', 'Direct Expenses': 'expense', 'Indirect Expenses': 'expense',
}
# primary groups that belong to the Trading account (gross profit) section
TRADING_GROUPS = {'Sales Accounts', 'Purchase Accounts', 'Direct Incomes', 'Direct Expenses'}


def _f(value):
    return float(value or 0)


def group_info():
    """group name -> {'primary': ..., 'nature': ...}  (also works for custom groups)."""
    info = {}
    for g in AccountGroup.objects.all():
        primary = g.primary_group or g.name
        nature = PRIMARY_NATURE.get(primary)
        if nature is None:  # custom primary group: guess from its flags
            if g.is_revenue:
                nature = 'expense' if g.is_deemed_positive else 'income'
            else:
                nature = 'asset' if g.is_deemed_positive else 'liability'
        info[g.name] = {'primary': primary, 'nature': nature}
    return info


def _sums(date_filter):
    """{ledger_name: [debit_total, credit_total]} for active vouchers matching date_filter."""
    out = defaultdict(lambda: [ZERO, ZERO])
    qs = (AccountingEntry.objects.filter(voucher__status='active').filter(date_filter)
          .values('ledger', 'is_dr').annotate(total=Sum('amount')))
    for row in qs:
        out[row['ledger']][0 if row['is_dr'] else 1] += row['total'] or ZERO
    return out


def ledger_rows(date_from=None, date_to=None):
    """One dict per ledger with opening, period debit/credit and closing (signed)."""
    info = group_info()
    before = _sums(Q(voucher__date__lt=date_from)) if date_from else {}
    period_q = Q()
    if date_from:
        period_q &= Q(voucher__date__gte=date_from)
    if date_to:
        period_q &= Q(voucher__date__lte=date_to)
    period = _sums(period_q)

    rows, seen = [], set()
    ledgers = list(Ledger.objects.filter(is_active=True).order_by('name'))
    names = {l.name for l in ledgers}
    # entries that use a ledger name which has no Ledger row are still shown
    extra = [n for n in set(before) | set(period) if n not in names]

    def build(name, group, opening_balance, opening_type):
        base = Decimal(opening_balance or 0)
        opening = base if (opening_type or 'dr').lower().startswith('d') else -base
        b = before.get(name, (ZERO, ZERO)) if date_from else (ZERO, ZERO)
        opening += b[0] - b[1]
        p = period.get(name, (ZERO, ZERO))
        closing = opening + p[0] - p[1]
        gi = info.get(group, {'primary': group or '(no group)', 'nature': 'unclassified'})
        return {'ledger': name, 'group': group or '(no group)', 'primary_group': gi['primary'],
                'nature': gi['nature'], 'opening': opening, 'debit': p[0], 'credit': p[1], 'closing': closing}

    for l in ledgers:
        rows.append(build(l.name, l.parent, l.opening_balance, l.opening_balance_type))
    for name in sorted(extra):
        rows.append(build(name, '', 0, 'dr'))
    return rows


def _dr_cr(signed):
    return (_f(signed), 0.0) if signed >= 0 else (0.0, _f(-signed))


def trial_balance(date_from=None, date_to=None):
    rows, totals = [], defaultdict(float)
    for r in ledger_rows(date_from, date_to):
        if not (r['opening'] or r['debit'] or r['credit'] or r['closing']):
            continue
        o_dr, o_cr = _dr_cr(r['opening'])
        c_dr, c_cr = _dr_cr(r['closing'])
        rows.append({'ledger': r['ledger'], 'group': r['group'], 'opening_dr': o_dr, 'opening_cr': o_cr,
                     'debit': _f(r['debit']), 'credit': _f(r['credit']), 'closing_dr': c_dr, 'closing_cr': c_cr})
        for k in ('opening_dr', 'opening_cr', 'debit', 'credit', 'closing_dr', 'closing_cr'):
            totals[k] += rows[-1][k]
    totals = {k: round(v, 2) for k, v in totals.items()}
    return {'from': date_from, 'to': date_to, 'rows': rows, 'totals': totals,
            'is_balanced': abs(totals.get('closing_dr', 0) - totals.get('closing_cr', 0)) < 0.01}


def _section(items):
    """[(group, ledger, amount)] -> [{'group','amount','ledgers':[...]}] without zero lines."""
    groups = defaultdict(list)
    for group, ledger, amount in items:
        if amount:
            groups[group].append({'ledger': ledger, 'amount': round(_f(amount), 2)})
    return [{'group': g, 'amount': round(sum(x['amount'] for x in ls), 2), 'ledgers': ls}
            for g, ls in sorted(groups.items())]


def profit_loss(date_from=None, date_to=None):
    income_t, expense_t, income_p, expense_p = [], [], [], []
    for r in ledger_rows(date_from, date_to):
        move = r['debit'] - r['credit']          # Dr - Cr in the period
        if r['nature'] == 'income':
            target = income_t if r['primary_group'] in TRADING_GROUPS else income_p
            target.append((r['group'], r['ledger'], -move))
        elif r['nature'] == 'expense':
            target = expense_t if r['primary_group'] in TRADING_GROUPS else expense_p
            target.append((r['group'], r['ledger'], move))
    trading = {'income': _section(income_t), 'expense': _section(expense_t)}
    trading['total_income'] = round(sum(g['amount'] for g in trading['income']), 2)
    trading['total_expense'] = round(sum(g['amount'] for g in trading['expense']), 2)
    gross = round(trading['total_income'] - trading['total_expense'], 2)
    pl = {'income': _section(income_p), 'expense': _section(expense_p)}
    pl['total_income'] = round(sum(g['amount'] for g in pl['income']), 2)
    pl['total_expense'] = round(sum(g['amount'] for g in pl['expense']), 2)
    net = round(gross + pl['total_income'] - pl['total_expense'], 2)
    return {'from': date_from, 'to': date_to, 'trading': trading, 'gross_profit': gross,
            'profit_loss': pl, 'net_profit': net,
            'note': 'Closing stock is not valued automatically - enter it as a ledger if you need it.'}


def balance_sheet(date_from=None, date_to=None):
    """Assets and liabilities as on date_to.  Profit of [date_from, date_to] is added to liabilities."""
    assets, liabilities = [], []
    for r in ledger_rows(None, date_to):          # opening of books + everything up to date_to
        if r['nature'] == 'asset':
            assets.append((r['group'], r['ledger'], r['closing']))
        elif r['nature'] in ('liability', 'unclassified'):
            liabilities.append((r['group'], r['ledger'], -r['closing']))
    net = profit_loss(date_from, date_to)['net_profit']
    liabilities_sec = _section(liabilities)
    if net:
        liabilities_sec.append({'group': 'Profit & Loss A/c', 'amount': net,
                                'ledgers': [{'ledger': 'Net profit for the period', 'amount': net}]})
    assets_sec = _section(assets)
    total_assets = round(sum(g['amount'] for g in assets_sec), 2)
    total_liab = round(sum(g['amount'] for g in liabilities_sec), 2)
    return {'from': date_from, 'to': date_to, 'assets': assets_sec, 'liabilities': liabilities_sec,
            'total_assets': total_assets, 'total_liabilities': total_liab,
            'difference': round(total_assets - total_liab, 2)}
