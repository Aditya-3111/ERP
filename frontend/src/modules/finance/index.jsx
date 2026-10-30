// Finance module: ledgers, account groups, voucher types (simple tables) + vouchers and reports (custom pages).
import { accountGroups, ledgers, voucherTypes } from './resources.js';
import BalanceSheetPage from './pages/BalanceSheetPage.jsx';
import LedgerStatementPage from './pages/LedgerStatementPage.jsx';
import ProfitLossPage from './pages/ProfitLossPage.jsx';
import TrialBalancePage from './pages/TrialBalancePage.jsx';
import VoucherFormPage from './pages/VoucherFormPage.jsx';
import VouchersPage from './pages/VouchersPage.jsx';

export default {
  key: 'finance',
  title: 'Finance',
  icon: 'finance',
  // tables shown by the shared <ResourcePage>  ->  /finance/<key>
  resources: [
    { ...ledgers, rowActions: [{ label: 'Statement', to: (row) => `/finance/ledgers/${row.guid}/statement` }] },
    accountGroups,
    voucherTypes,
  ],
  // pages written by hand  ->  /finance/<path>
  routes: [
    { path: 'vouchers', element: <VouchersPage /> },
    { path: 'vouchers/new', element: <VoucherFormPage /> },
    { path: 'vouchers/:id', element: <VoucherFormPage /> },
    { path: 'ledgers/:id/statement', element: <LedgerStatementPage /> },
    { path: 'reports/trial-balance', element: <TrialBalancePage /> },
    { path: 'reports/profit-loss', element: <ProfitLossPage /> },
    { path: 'reports/balance-sheet', element: <BalanceSheetPage /> },
  ],
  menu: [
    { label: 'Vouchers', path: '/finance/vouchers' },
    { label: 'Ledgers', path: '/finance/ledgers' },
    { label: 'Account Groups', path: '/finance/account-groups' },
    { label: 'Voucher Types', path: '/finance/voucher-types' },
    { label: 'Trial Balance', path: '/finance/reports/trial-balance' },
    { label: 'Profit & Loss', path: '/finance/reports/profit-loss' },
    { label: 'Balance Sheet', path: '/finance/reports/balance-sheet' },
  ],
};
