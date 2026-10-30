import Badge from '../ui/Badge.jsx';
import { formatDate, formatDateTime, formatMoney, formatNumber } from '../../utils/format.js';

/** Show one table cell according to the column `type` from the resource config. */
export function renderCell(column, row) {
  const value = row[column.key];
  switch (column.type) {
    case 'date': return formatDate(value);
    case 'datetime': return formatDateTime(value);
    case 'money': return <span className="tabular-nums">{formatMoney(value)}</span>;
    case 'number': return <span className="tabular-nums">{formatNumber(value)}</span>;
    case 'bool': return value ? <span className="text-emerald-600">Yes</span> : <span className="text-slate-400">No</span>;
    case 'badge': return <Badge value={value} />;
    default: return value === null || value === undefined || value === '' ? <span className="text-slate-400">-</span> : String(value);
  }
}

/**
 * Plain table.  columns: [{ key, label, type? }]   rows: array from the API
 * `actions(row)` returns the buttons for the last column.
 */
export default function DataTable({ columns, rows, actions, rowKey = 'guid' }) {
  const alignRight = (c) => c.type === 'money' || c.type === 'number';
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-slate-200">
        <thead>
          <tr>
            {columns.map((c) => <th key={c.key} className={`th ${alignRight(c) ? 'text-right' : ''}`}>{c.label}</th>)}
            {actions && <th className="th text-right">Actions</th>}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {rows.map((row, i) => (
            <tr key={row[rowKey] ?? i} className="hover:bg-slate-50">
              {columns.map((c) => <td key={c.key} className={`td ${alignRight(c) ? 'text-right' : ''}`}>{renderCell(c, row)}</td>)}
              {actions && <td className="td whitespace-nowrap text-right">{actions(row)}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
