import { Card } from '../../../components/ui/Card.jsx';
import { formatMoney } from '../../../utils/format.js';
import ReportShell from './ReportShell.jsx';

const money = (n) => (n ? formatMoney(n) : '');

export default function TrialBalancePage() {
  return (
    <ReportShell title="Trial Balance" subtitle="Opening, movement and closing balance of every ledger" endpoint="/finance/reports/trial-balance/">
      {(tb) => (
        <Card bodyClassName="p-0">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead>
                <tr><th className="th" rowSpan={2}>Ledger</th><th className="th" rowSpan={2}>Group</th>
                  <th className="th text-center" colSpan={2}>Opening</th><th className="th text-center" colSpan={2}>Period</th><th className="th text-center" colSpan={2}>Closing</th></tr>
                <tr>{['Dr', 'Cr', 'Debit', 'Credit', 'Dr', 'Cr'].map((h, i) => <th key={i} className="th text-right">{h}</th>)}</tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {tb.rows.map((r) => (
                  <tr key={r.ledger}>
                    <td className="td font-medium">{r.ledger}</td><td className="td text-slate-500">{r.group}</td>
                    {[r.opening_dr, r.opening_cr, r.debit, r.credit, r.closing_dr, r.closing_cr].map((v, i) => <td key={i} className="td text-right tabular-nums">{money(v)}</td>)}
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="bg-slate-50 font-semibold">
                  <td className="td" colSpan={2}>Total</td>
                  {['opening_dr', 'opening_cr', 'debit', 'credit', 'closing_dr', 'closing_cr'].map((k) => <td key={k} className="td text-right tabular-nums">{formatMoney(tb.totals[k] || 0)}</td>)}
                </tr>
              </tfoot>
            </table>
          </div>
          <p className={`px-5 py-3 text-sm font-semibold ${tb.is_balanced ? 'text-emerald-600' : 'text-red-600'}`} data-testid="tb-state">
            {tb.is_balanced ? 'Trial balance is balanced (closing Dr = closing Cr).' : 'Trial balance does NOT balance - check opening balances.'}
          </p>
        </Card>
      )}
    </ReportShell>
  );
}
