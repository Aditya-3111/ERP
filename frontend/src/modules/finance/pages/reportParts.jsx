import { formatMoney } from '../../../utils/format.js';

/** A list of account groups, each with its ledgers underneath (used by P&L and Balance Sheet). */
export function GroupList({ groups, empty = 'Nothing to show' }) {
  if (!groups.length) return <p className="px-5 py-4 text-sm text-slate-400">{empty}</p>;
  return (
    <ul className="divide-y divide-slate-100">
      {groups.map((g) => (
        <li key={g.group} className="px-5 py-3">
          <div className="flex justify-between font-medium text-slate-800"><span>{g.group}</span><span className="tabular-nums">{formatMoney(g.amount)}</span></div>
          <ul className="mt-1 space-y-0.5 pl-4 text-sm text-slate-500">
            {g.ledgers.map((l) => <li key={l.ledger} className="flex justify-between"><span>{l.ledger}</span><span className="tabular-nums">{formatMoney(l.amount)}</span></li>)}
          </ul>
        </li>
      ))}
    </ul>
  );
}

export function TotalRow({ label, amount, tone = 'slate' }) {
  const color = { slate: 'text-slate-900', green: 'text-emerald-700', red: 'text-red-700' }[tone];
  return (
    <div className={`flex justify-between border-t border-slate-200 bg-slate-50 px-5 py-3 font-semibold ${color}`}>
      <span>{label}</span><span className="tabular-nums">{formatMoney(amount)}</span>
    </div>
  );
}
