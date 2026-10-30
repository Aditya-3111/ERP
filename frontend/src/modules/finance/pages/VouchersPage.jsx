import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api, rowsOf } from '../../../api/client.js';
import DataTable from '../../../components/crud/DataTable.jsx';
import Alert from '../../../components/ui/Alert.jsx';
import Button from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import ConfirmDialog from '../../../components/ui/ConfirmDialog.jsx';
import EmptyState from '../../../components/ui/EmptyState.jsx';
import Icon from '../../../components/ui/Icon.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Pagination from '../../../components/ui/Pagination.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import { usePeriod } from '../../../context/PeriodContext.jsx';
import { useToast } from '../../../context/ToastContext.jsx';
import useDebounce from '../../../hooks/useDebounce.js';
import useLookup from '../../../hooks/useLookup.js';

const COLUMNS = [
  { key: 'date', label: 'Date', type: 'date' },
  { key: 'voucher_number', label: 'Number' },
  { key: 'voucher_type', label: 'Type', type: 'badge' },
  { key: 'party_name', label: 'Party' },
  { key: 'narration', label: 'Narration' },
  { key: 'amount', label: 'Amount', type: 'money' },
  { key: 'status', label: 'Status', type: 'badge' },
];

/** List of vouchers for the selected financial year, with filters. */
export default function VouchersPage() {
  const { period } = usePeriod();
  const toast = useToast();
  const navigate = useNavigate();
  const types = useLookup('voucherTypes');
  const [type, setType] = useState('');
  const [text, setText] = useState('');
  const search = useDebounce(text);
  const [page, setPage] = useState(1);
  const [state, setState] = useState({ rows: [], count: 0, loading: true, error: null });
  const [deleting, setDeleting] = useState(null);

  const load = useCallback(() => {
    setState((s) => ({ ...s, loading: true, error: null }));
    api.get('/finance/vouchers/', { page, search, voucher_type: type, from: period.from, to: period.to })
      .then((data) => setState({
        // the list shows the total of the debit side as the voucher amount
        rows: rowsOf(data).map((v) => ({ ...v, amount: (v.items || []).filter((i) => i.is_dr).reduce((s, i) => s + Number(i.amount), 0) })),
        count: data.count ?? 0, loading: false, error: null,
      }))
      .catch((error) => setState({ rows: [], count: 0, loading: false, error }));
  }, [page, search, type, period.from, period.to]);

  useEffect(() => { load(); }, [load]);
  useEffect(() => { setPage(1); }, [search, type, period.from, period.to]);

  async function remove() {
    try {
      await api.delete(`/finance/vouchers/${deleting.guid}/`);
      toast.success('Voucher deleted.');
      setDeleting(null);
      load();
    } catch (err) {
      toast.error(err.message);
      setDeleting(null);
    }
  }

  const actions = (row) => (
    <div className="flex justify-end gap-1">
      <Link to={`/finance/vouchers/${row.guid}`} className="btn btn-ghost btn-sm" aria-label="Open voucher"><Icon name="edit" className="h-4 w-4" /></Link>
      <button type="button" className="btn btn-ghost btn-sm text-red-600" onClick={() => setDeleting(row)} aria-label="Delete voucher"><Icon name="trash" className="h-4 w-4" /></button>
    </div>
  );

  return (
    <>
      <PageHeader title="Vouchers" subtitle={`${period.name}  |  ${state.count} voucher${state.count === 1 ? '' : 's'}`}>
        <Button icon="plus" onClick={() => navigate('/finance/vouchers/new')}>New voucher</Button>
      </PageHeader>
      <Card bodyClassName="p-0">
        <div className="flex flex-wrap items-center gap-3 border-b border-slate-200 p-4">
          <div className="relative w-full max-w-xs">
            <Icon name="search" className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
            <input className="input pl-9" placeholder="Search number, party, narration..." value={text} onChange={(e) => setText(e.target.value)} aria-label="Search" />
          </div>
          <select className="input w-auto" value={type} onChange={(e) => setType(e.target.value)} aria-label="Voucher type">
            <option value="">All types</option>
            {types.options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </div>
        {state.error && <div className="p-4"><Alert onRetry={load}>{state.error.message}</Alert></div>}
        {state.loading && <Spinner />}
        {!state.loading && !state.error && state.rows.length === 0 && <EmptyState title="No vouchers in this period" hint='Click "New voucher" to enter the first one.' />}
        {!state.loading && state.rows.length > 0 && (
          <>
            <DataTable columns={COLUMNS} rows={state.rows} actions={actions} />
            <Pagination page={page} count={state.count} onPage={setPage} />
          </>
        )}
      </Card>
      {deleting && <ConfirmDialog message={`Delete voucher ${deleting.voucher_number}? Its accounting entries are deleted too.`} onConfirm={remove} onCancel={() => setDeleting(null)} />}
    </>
  );
}
