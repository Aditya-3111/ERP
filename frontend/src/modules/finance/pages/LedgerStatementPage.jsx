import { useParams } from 'react-router-dom';
import { api } from '../../../api/client.js';
import Alert from '../../../components/ui/Alert.jsx';
import Button from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import EmptyState from '../../../components/ui/EmptyState.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import useFetch from '../../../hooks/useFetch.js';
import { formatDate, formatMoney } from '../../../utils/format.js';

/** Dr balance is shown with "Dr", Cr balance with "Cr". */
const withSide = (n) => `${formatMoney(Math.abs(n))} ${n >= 0 ? 'Dr' : 'Cr'}`;

export default function LedgerStatementPage() {
  const { id } = useParams();
  const { data, loading, error, reload } = useFetch(async () => {
    const [ledger, rows] = await Promise.all([api.get(`/finance/ledgers/${id}/`), api.get(`/finance/ledgers/${id}/transactions/`)]);
    return { ledger, rows };
  }, [id]);

  if (loading) return <Spinner />;
  if (error) return <Alert onRetry={reload}>{error.message}</Alert>;
  const { ledger, rows } = data;
  const opening = Number(ledger.opening_balance) * (String(ledger.opening_balance_type).toLowerCase().startsWith('d') ? 1 : -1);

  return (
    <>
      <PageHeader title={ledger.name} subtitle={`Ledger statement  |  Group: ${ledger.parent || '-'}`}>
        <Button variant="secondary" onClick={() => window.print()}>Print</Button>
      </PageHeader>
      <Card bodyClassName="p-0">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead><tr>
              <th className="th">Date</th><th className="th">Voucher</th><th className="th">Type</th><th className="th">Particulars</th>
              <th className="th text-right">Debit</th><th className="th text-right">Credit</th><th className="th text-right">Balance</th>
            </tr></thead>
            <tbody className="divide-y divide-slate-100">
              <tr className="bg-slate-50"><td className="td" colSpan={6}>Opening balance</td><td className="td text-right tabular-nums">{withSide(opening)}</td></tr>
              {rows.map((r, i) => (
                <tr key={i}>
                  <td className="td">{formatDate(r.date)}</td><td className="td">{r.voucher_number}</td><td className="td">{r.voucher_type}</td><td className="td">{r.particulars || '-'}</td>
                  <td className="td text-right tabular-nums">{r.debit ? formatMoney(r.debit) : ''}</td>
                  <td className="td text-right tabular-nums">{r.credit ? formatMoney(r.credit) : ''}</td>
                  <td className="td text-right tabular-nums">{withSide(r.balance)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {rows.length === 0 && <EmptyState title="No transactions yet" />}
        <div className="border-t border-slate-200 bg-slate-50 px-5 py-3 text-right text-sm">
          Closing balance: <b className="tabular-nums" data-testid="closing-balance">{withSide(Number(ledger.current_balance ?? opening))}</b>
        </div>
      </Card>
    </>
  );
}
