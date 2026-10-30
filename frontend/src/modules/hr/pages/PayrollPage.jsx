import { useState } from 'react';
import { api } from '../../../api/client.js';
import Alert from '../../../components/ui/Alert.jsx';
import { Card } from '../../../components/ui/Card.jsx';
import EmptyState from '../../../components/ui/EmptyState.jsx';
import PageHeader from '../../../components/ui/PageHeader.jsx';
import Spinner from '../../../components/ui/Spinner.jsx';
import useFetch from '../../../hooks/useFetch.js';
import { formatMoney, todayISO } from '../../../utils/format.js';

/** Monthly salary summary. Deduction = one day's pay for every absent day (half a day for "Half Day"). */
export default function PayrollPage() {
  const [month, setMonth] = useState(todayISO().slice(0, 7));
  const { data, loading, error, reload } = useFetch(() => api.get('/hr/payroll/', { month }), [month]);
  const rows = data?.results || [];
  const total = rows.reduce((s, r) => s + r.net_salary, 0);

  return (
    <>
      <PageHeader title="Payroll" subtitle="Monthly salary summary calculated from attendance">
        <input type="month" className="input w-auto" value={month} onChange={(e) => e.target.value && setMonth(e.target.value)} aria-label="Month" />
      </PageHeader>
      {error && <Alert onRetry={reload}>{error.message}</Alert>}
      {loading ? <Spinner /> : (
        <Card bodyClassName="p-0">
          {rows.length === 0 ? <EmptyState title="No active employees" /> : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200">
                <thead><tr>
                  <th className="th">Code</th><th className="th">Employee</th><th className="th">Department</th>
                  <th className="th text-right">Absent</th><th className="th text-right">Half days</th>
                  <th className="th text-right">Basic</th><th className="th text-right">Deductions</th><th className="th text-right">Net salary</th>
                </tr></thead>
                <tbody className="divide-y divide-slate-100">
                  {rows.map((r) => (
                    <tr key={r.employee}>
                      <td className="td">{r.emp_code}</td><td className="td font-medium">{r.employee_name}</td><td className="td text-slate-500">{r.department}</td>
                      <td className="td text-right">{r.absent_days}</td><td className="td text-right">{r.half_days}</td>
                      <td className="td text-right tabular-nums">{formatMoney(r.basic)}</td>
                      <td className="td text-right tabular-nums text-red-600">{formatMoney(r.deductions)}</td>
                      <td className="td text-right font-semibold tabular-nums">{formatMoney(r.net_salary)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot><tr className="bg-slate-50 font-semibold"><td className="td" colSpan={7}>Total payable</td><td className="td text-right tabular-nums" data-testid="payroll-total">{formatMoney(total)}</td></tr></tfoot>
              </table>
            </div>
          )}
        </Card>
      )}
    </>
  );
}
