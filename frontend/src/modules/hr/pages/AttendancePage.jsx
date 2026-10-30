import { useEffect, useState } from 'react';
import { api, rowsOf } from '../../../api/client.js';
import Alert from '../../../components/ui/Alert.jsx';
import Button from '../../../components/ui/Button.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import EmptyState from '../../../components/ui/EmptyState.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import { useToast } from '../../../context/ToastContext.jsx';
import { todayISO } from '../../../utils/format.js';

const STATUSES = ['Present', 'Absent', 'Half Day', 'Leave', 'Holiday'];

/** Mark attendance of all active employees for one day, then save everything in ONE request. */
export default function AttendancePage() {
  const toast = useToast();
  const [date, setDate] = useState(todayISO());
  const [rows, setRows] = useState([]);          // [{employee, name, code, status, in_time, out_time}]
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError('');
    Promise.all([
      api.get('/hr/employees/', { status: 'active', page_size: 500, ordering: 'emp_code' }),
      api.get('/hr/attendance/', { date, page_size: 500 }),
    ]).then(([emps, att]) => {
      if (!alive) return;
      const saved = new Map(rowsOf(att).map((a) => [a.employee, a]));
      setRows(rowsOf(emps).map((e) => {
        const a = saved.get(e.guid);
        return {
          employee: e.guid, code: e.emp_code, name: e.name, department: e.department,
          status: a ? a.status : 'Present',
          in_time: a?.in_time ? a.in_time.slice(0, 5) : '', out_time: a?.out_time ? a.out_time.slice(0, 5) : '',
          existing: Boolean(a),
        };
      }));
    }).catch((e) => alive && setError(e.message)).finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [date]);

  const update = (i, patch) => setRows((list) => list.map((r, n) => (n === i ? { ...r, ...patch } : r)));

  async function save() {
    setSaving(true);
    try {
      const result = await api.post('/hr/attendance/bulk/', {
        attendances: rows.map((r) => ({ employee: r.employee, date, status: r.status, in_time: r.in_time || null, out_time: r.out_time || null })),
      });
      toast.success(`Attendance saved (${result.created} new, ${result.updated} updated).`);
    } catch (e) {
      toast.error(e.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <PageHeader title="Mark Attendance" subtitle="Pick a date, set each employee's status, press Save.">
        <input type="date" className="input w-auto" value={date} max={todayISO()} onChange={(e) => setDate(e.target.value)} aria-label="Date" />
        <Button variant="secondary" onClick={() => setRows((l) => l.map((r) => ({ ...r, status: 'Present' })))}>All present</Button>
        <Button onClick={save} loading={saving} disabled={!rows.length}>Save attendance</Button>
      </PageHeader>
      {error && <Alert>{error}</Alert>}
      {loading ? <Spinner /> : (
        <Card bodyClassName="p-0">
          {rows.length === 0 ? <EmptyState title="No active employees" hint="Add employees under HR -> Employees first." /> : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200">
                <thead><tr><th className="th">Code</th><th className="th">Employee</th><th className="th">Department</th><th className="th">Status</th><th className="th">In</th><th className="th">Out</th></tr></thead>
                <tbody className="divide-y divide-slate-100">
                  {rows.map((r, i) => (
                    <tr key={r.employee}>
                      <td className="td">{r.code}</td><td className="td font-medium">{r.name}</td><td className="td text-slate-500">{r.department}</td>
                      <td className="td"><select className="input w-36" value={r.status} onChange={(e) => update(i, { status: e.target.value })} aria-label={`Status of ${r.name}`}>
                        {STATUSES.map((s) => <option key={s}>{s}</option>)}</select></td>
                      <td className="td"><input type="time" className="input w-32" value={r.in_time} onChange={(e) => update(i, { in_time: e.target.value })} aria-label={`In time of ${r.name}`} /></td>
                      <td className="td"><input type="time" className="input w-32" value={r.out_time} onChange={(e) => update(i, { out_time: e.target.value })} aria-label={`Out time of ${r.name}`} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      )}
    </>
  );
}
