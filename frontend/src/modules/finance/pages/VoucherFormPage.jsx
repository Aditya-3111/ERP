import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../../../api/client.js';
import Alert from '../../../components/ui/Alert.jsx';
import Button from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import Icon from '../../../components/ui/Icon.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import { useToast } from '../../../context/ToastContext.jsx';
import useLookup from '../../../hooks/useLookup.js';
import { formatMoney, todayISO } from '../../../utils/format.js';

const emptyLine = () => ({ ledger: '', amount: '', is_dr: true });
const TYPES = ['Sales', 'Purchase', 'Receipt', 'Payment', 'Journal', 'Contra', 'Credit Note', 'Debit Note'];

/**
 * Create or edit ONE voucher with its debit / credit lines (double entry).
 * The Save button works only when total Debit = total Credit.
 */
export default function VoucherFormPage() {
  const { id } = useParams();                       // undefined on /vouchers/new
  const editing = Boolean(id);
  const navigate = useNavigate();
  const toast = useToast();
  const ledgers = useLookup('ledgers');
  const typeLookup = useLookup('voucherTypes');
  const [loading, setLoading] = useState(editing);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [head, setHead] = useState({
    voucher_type: 'Sales', date: todayISO(), voucher_number: '', party_name: '',
    reference_number: '', narration: '', status: 'active',
  });
  const [lines, setLines] = useState([{ ...emptyLine(), is_dr: true }, { ...emptyLine(), is_dr: false }]);

  useEffect(() => {
    if (!editing) return;
    api.get(`/finance/vouchers/${id}/`)
      .then((v) => {
        setHead({
          voucher_type: v.voucher_type, date: v.date, voucher_number: v.voucher_number, party_name: v.party_name || '',
          reference_number: v.reference_number || '', narration: v.narration || '', status: v.status,
        });
        setLines((v.items || []).map((i) => ({ ledger: i.ledger, amount: String(i.amount), is_dr: i.is_dr })));
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [editing, id]);

  const totals = useMemo(() => {
    let dr = 0; let cr = 0;
    for (const l of lines) {
      const n = Number(l.amount) || 0;
      if (l.is_dr) dr += n; else cr += n;
    }
    return { dr, cr, diff: Math.round((dr - cr) * 100) / 100 };
  }, [lines]);

  const usable = lines.filter((l) => l.ledger && Number(l.amount) > 0);
  const canSave = usable.length >= 2 && totals.diff === 0 && totals.dr > 0;

  const setLine = (index, patch) => setLines((list) => list.map((l, i) => (i === index ? { ...l, ...patch } : l)));
  const setField = (name, value) => setHead((h) => ({ ...h, [name]: value }));
  const typeNames = typeLookup.options.length ? typeLookup.options.map((o) => o.value) : TYPES;

  async function save(e) {
    e.preventDefault();
    setSaving(true);
    setError('');
    const body = {
      ...head,
      voucher_number: head.voucher_number || '',
      items: usable.map((l) => ({ ledger: l.ledger, amount: Number(l.amount), is_dr: l.is_dr })),
    };
    try {
      if (editing) await api.patch(`/finance/vouchers/${id}/`, body);
      else await api.post('/finance/vouchers/', body);
      toast.success(editing ? 'Voucher updated.' : 'Voucher saved.');
      navigate('/finance/vouchers');
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <Spinner />;

  return (
    <form onSubmit={save} noValidate>
      <PageHeader title={editing ? `Voucher ${head.voucher_number}` : 'New voucher'} subtitle="Every voucher needs equal debit and credit totals.">
        <Button variant="secondary" onClick={() => navigate('/finance/vouchers')}>Cancel</Button>
        <Button type="submit" loading={saving} disabled={!canSave}>Save voucher</Button>
      </PageHeader>
      {error && <div className="mb-4"><Alert>{error}</Alert></div>}

      <Card title="Details" className="mb-5">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div>
            <label className="label" htmlFor="voucher_type">Voucher type</label>
            <select id="voucher_type" className="input" value={head.voucher_type} onChange={(e) => setField('voucher_type', e.target.value)}>
              {typeNames.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label className="label" htmlFor="date">Date</label>
            <input id="date" type="date" className="input" value={head.date} onChange={(e) => setField('date', e.target.value)} required />
          </div>
          <div>
            <label className="label" htmlFor="voucher_number">Number</label>
            <input id="voucher_number" className="input" placeholder="Automatic" value={head.voucher_number} onChange={(e) => setField('voucher_number', e.target.value)} />
          </div>
          <div>
            <label className="label" htmlFor="party_name">Party name</label>
            <input id="party_name" className="input" value={head.party_name} onChange={(e) => setField('party_name', e.target.value)} />
          </div>
          <div>
            <label className="label" htmlFor="reference_number">Reference no.</label>
            <input id="reference_number" className="input" value={head.reference_number} onChange={(e) => setField('reference_number', e.target.value)} />
          </div>
          {editing && (
            <div>
              <label className="label" htmlFor="status">Status</label>
              <select id="status" className="input" value={head.status} onChange={(e) => setField('status', e.target.value)}>
                <option value="active">Active</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          )}
          <div className="md:col-span-3">
            <label className="label" htmlFor="narration">Narration</label>
            <textarea id="narration" rows={2} className="input" value={head.narration} onChange={(e) => setField('narration', e.target.value)} />
          </div>
        </div>
      </Card>

      <Card title="Entries" bodyClassName="p-0"
        actions={<Button size="sm" variant="secondary" icon="plus" onClick={() => setLines((l) => [...l, emptyLine()])}>Add line</Button>}>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead><tr><th className="th w-28">Dr / Cr</th><th className="th">Ledger</th><th className="th w-48 text-right">Amount</th><th className="th w-12" /></tr></thead>
            <tbody className="divide-y divide-slate-100">
              {lines.map((l, i) => (
                <tr key={i}>
                  <td className="td">
                    <select className="input" value={l.is_dr ? 'dr' : 'cr'} onChange={(e) => setLine(i, { is_dr: e.target.value === 'dr' })} aria-label={`Line ${i + 1} Dr or Cr`}>
                      <option value="dr">Dr</option><option value="cr">Cr</option>
                    </select>
                  </td>
                  <td className="td">
                    <select className="input" value={l.ledger} onChange={(e) => setLine(i, { ledger: e.target.value })} aria-label={`Line ${i + 1} ledger`}>
                      <option value="">- select ledger -</option>
                      {ledgers.options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                    </select>
                  </td>
                  <td className="td">
                    <input type="number" min="0" step="0.01" className="input text-right" value={l.amount} onChange={(e) => setLine(i, { amount: e.target.value })} aria-label={`Line ${i + 1} amount`} />
                  </td>
                  <td className="td">
                    {lines.length > 2 && (
                      <button type="button" className="btn btn-ghost btn-sm text-red-600" onClick={() => setLines((list) => list.filter((_, n) => n !== i))} aria-label={`Remove line ${i + 1}`}>
                        <Icon name="trash" className="h-4 w-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex flex-wrap items-center justify-end gap-6 border-t border-slate-200 bg-slate-50 px-5 py-3 text-sm">
          <span>Debit: <b className="tabular-nums">{formatMoney(totals.dr)}</b></span>
          <span>Credit: <b className="tabular-nums">{formatMoney(totals.cr)}</b></span>
          {totals.diff === 0 && totals.dr > 0
            ? <span className="font-semibold text-emerald-600" data-testid="balance-state">Balanced</span>
            : <span className="font-semibold text-red-600" data-testid="balance-state">Difference {formatMoney(Math.abs(totals.diff))}</span>}
        </div>
      </Card>
    </form>
  );
}
