import { Link } from 'react-router-dom';
import { api } from '../api/client.js';
import Alert from '../components/ui/Alert.jsx';
import Badge from '../components/ui/Badge.jsx';
import { Card, StatCard } from '../components/ui/Card.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import Spinner from '../components/ui/Spinner.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { usePeriod } from '../context/PeriodContext.jsx';
import useFetch from '../hooks/useFetch.js';
import { formatDate, formatMoney, formatMoneyWhole, formatNumber } from '../utils/format.js';

/** Two bars per month (sales, purchase) drawn with plain divs - no chart library needed. */
function MonthlyBars({ months }) {
  const max = Math.max(1, ...months.flatMap((m) => [m.sales, m.purchase]));
  return (
    <div>
      <div className="flex h-48 items-end gap-3">
        {months.map((m) => (
          <div key={m.month} className="flex flex-1 flex-col items-center gap-1">
            <div className="flex h-40 w-full items-end justify-center gap-1">
              <div className="w-1/3 rounded-t bg-brand-500" style={{ height: `${(m.sales / max) * 100}%` }} title={`Sales ${formatMoney(m.sales)}`} />
              <div className="w-1/3 rounded-t bg-amber-400" style={{ height: `${(m.purchase / max) * 100}%` }} title={`Purchase ${formatMoney(m.purchase)}`} />
            </div>
            <span className="text-xs text-slate-500">{m.month.split(' ')[0]}</span>
          </div>
        ))}
      </div>
      <div className="mt-3 flex gap-4 text-xs text-slate-500">
        <span className="flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-sm bg-brand-500" /> Sales</span>
        <span className="flex items-center gap-1"><span className="h-2.5 w-2.5 rounded-sm bg-amber-400" /> Purchase</span>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  const { period } = usePeriod();
  const { data: d, loading, error, reload } = useFetch(() => api.get('/core/dashboard/', { from: period.from, to: period.to }), [period.from, period.to]);

  return (
    <>
      <PageHeader title={`Welcome, ${user?.fullname?.trim() || user?.username}`} subtitle={`${period.name}  |  ${formatDate(period.from)} to ${formatDate(period.to)}`} />
      {error && <Alert onRetry={reload}>{error.message}</Alert>}
      {loading && <Spinner />}
      {d && (
        <div className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard label="Sales" value={formatMoneyWhole(d.finance.sales)} icon="trend" tone="indigo" />
            <StatCard label="Purchases" value={formatMoneyWhole(d.finance.purchase)} icon="receipt" tone="amber" />
            <StatCard label={d.finance.net_profit >= 0 ? 'Net profit' : 'Net loss'} value={formatMoneyWhole(d.finance.net_profit)} icon="scale" tone={d.finance.net_profit >= 0 ? 'green' : 'red'} />
            <StatCard label="Cash & bank" value={formatMoneyWhole(d.finance.cash_bank)} icon="wallet" tone="sky" />
            <StatCard label="Receivable" value={formatMoneyWhole(d.finance.receivable)} hint="Owed by customers" icon="file" tone="green" />
            <StatCard label="Payable" value={formatMoneyWhole(d.finance.payable)} hint="Owed to suppliers" icon="file" tone="red" />
            <StatCard label="Active employees" value={formatNumber(d.counts.employees)} hint={`Today: ${d.attendance_today.present} present, ${d.attendance_today.absent} absent`} icon="hr" tone="indigo" />
            <StatCard label="Open work orders" value={formatNumber(d.counts.open_work_orders)} hint={`${d.counts.visitors_inside} visitors inside`} icon="maintenance" tone="amber" />
          </div>

          <div className="grid gap-6 xl:grid-cols-3">
            <Card title="Sales vs purchase - last 6 months" className="xl:col-span-2"><MonthlyBars months={d.monthly} /></Card>
            <Card title="Low stock items" bodyClassName="p-0"
              actions={<Link to="/inventory/items" className="text-sm font-medium text-brand-600">All items</Link>}>
              {d.low_stock_items.length === 0 ? <p className="p-5 text-sm text-slate-500">All items are above their minimum level.</p> : (
                <ul className="divide-y divide-slate-100">
                  {d.low_stock_items.map((i) => (
                    <li key={i.guid} className="flex items-center justify-between px-5 py-3 text-sm">
                      <span className="font-medium text-slate-800">{i.name}</span>
                      <span className="text-red-600">{formatNumber(i.closing_balance)} / {formatNumber(i.min_stock)} {i.uom}</span>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          </div>

          <Card title="Recent vouchers" bodyClassName="p-0" actions={<Link to="/finance/vouchers" className="text-sm font-medium text-brand-600">All vouchers</Link>}>
            <table className="min-w-full divide-y divide-slate-200">
              <thead><tr><th className="th">Date</th><th className="th">Number</th><th className="th">Type</th><th className="th">Party</th><th className="th text-right">Amount</th></tr></thead>
              <tbody className="divide-y divide-slate-100">
                {d.recent_vouchers.map((v) => (
                  <tr key={v.guid} className="hover:bg-slate-50">
                    <td className="td">{formatDate(v.date)}</td>
                    <td className="td"><Link className="font-medium text-brand-600" to={`/finance/vouchers/${v.guid}`}>{v.voucher_number}</Link></td>
                    <td className="td"><Badge value={v.voucher_type} tone="slate" /></td>
                    <td className="td">{v.party_name || '-'}</td>
                    <td className="td text-right tabular-nums">{formatMoney(v.amount)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>
      )}
    </>
  );
}
