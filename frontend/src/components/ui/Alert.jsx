import Icon from './Icon.jsx';

const TONES = {
  error: 'border-red-200 bg-red-50 text-red-700',
  warning: 'border-amber-200 bg-amber-50 text-amber-800',
  info: 'border-sky-200 bg-sky-50 text-sky-800',
  success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
};

export default function Alert({ tone = 'error', children, onRetry }) {
  return (
    <div role="alert" className={`flex items-start gap-3 rounded-lg border px-4 py-3 text-sm ${TONES[tone]}`}>
      <Icon name={tone === 'info' ? 'info' : 'warning'} className="mt-0.5 h-4 w-4 shrink-0" />
      <div className="flex-1">{children}</div>
      {onRetry && <button type="button" className="font-semibold underline" onClick={onRetry}>Retry</button>}
    </div>
  );
}
