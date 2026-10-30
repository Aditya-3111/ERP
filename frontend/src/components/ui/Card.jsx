import Icon from './Icon.jsx';

export function Card({ title, actions, children, className = '', bodyClassName = 'p-5' }) {
  return (
    <section className={`card ${className}`}>
      {(title || actions) && (
        <header className="flex items-center justify-between border-b border-slate-200 px-5 py-3">
          <h2 className="font-semibold text-slate-800">{title}</h2>
          <div>{actions}</div>
        </header>
      )}
      <div className={bodyClassName}>{children}</div>
    </section>
  );
}

const TONES = {
  indigo: 'bg-indigo-50 text-indigo-600', green: 'bg-emerald-50 text-emerald-600',
  amber: 'bg-amber-50 text-amber-600', red: 'bg-red-50 text-red-600', sky: 'bg-sky-50 text-sky-600',
};

/** Number tile for dashboards. */
export function StatCard({ label, value, hint, icon = 'trend', tone = 'indigo' }) {
  return (
    <div className="card flex items-center gap-4 p-5">
      <div className={`rounded-xl p-3 ${TONES[tone]}`}><Icon name={icon} className="h-6 w-6" /></div>
      <div className="min-w-0">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</p>
        <p className="break-words text-xl font-bold text-slate-900">{value}</p>
        {hint && <p className="text-xs text-slate-500">{hint}</p>}
      </div>
    </div>
  );
}
