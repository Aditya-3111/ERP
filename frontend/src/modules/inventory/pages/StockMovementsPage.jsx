import { useParams } from 'react-router-dom';
import { api } from '../../../api/client.js';
import Alert from '../../../components/ui/Alert.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import EmptyState from '../../../components/ui/EmptyState.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import Badge from '../../../components/ui/Badge.jsx';
import useFetch from '../../../hooks/useFetch.js';
import { formatDate, formatNumber } from '../../../utils/format.js';

export default function StockMovementsPage() {
  const { id } = useParams();
  const { data, loading, error, reload } = useFetch(async () => {
    const [item, rows] = await Promise.all([api.get(`/inventory/items/${id}/`), api.get(`/inventory/items/${id}/movements/`)]);
    return { item, rows };
  }, [id]);

  if (loading) return <Spinner />;
  if (error) return <Alert onRetry={reload}>{error.message}</Alert>;
  const { item, rows } = data;
  return (
    <>
      <PageHeader title={item.name} subtitle={`Stock movements  |  Opening ${formatNumber(item.opening_balance)} ${item.uom}`} />
      <Card bodyClassName="p-0">
        {rows.length === 0 ? <EmptyState title="No movements yet" hint="Receipts (MRN) and POS sales appear here." /> : (
          <table className="min-w-full divide-y divide-slate-200">
            <thead><tr><th className="th">Date</th><th className="th">Type</th><th className="th">Reference</th><th className="th text-right">In</th><th className="th text-right">Out</th><th className="th text-right">Balance</th></tr></thead>
            <tbody className="divide-y divide-slate-100">
              {rows.map((r, i) => (
                <tr key={i}><td className="td">{formatDate(r.date)}</td><td className="td"><Badge value={r.type === 'IN' ? 'received' : 'cancelled'} tone={r.type === 'IN' ? 'green' : 'amber'} /></td>
                  <td className="td">{r.reference}</td><td className="td text-right">{r.quantity_in ? formatNumber(r.quantity_in) : ''}</td>
                  <td className="td text-right">{r.quantity_out ? formatNumber(r.quantity_out) : ''}</td><td className="td text-right font-medium">{formatNumber(r.balance)}</td></tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </>
  );
}
