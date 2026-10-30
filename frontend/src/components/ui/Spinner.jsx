export default function Spinner({ label = 'Loading...' }) {
  return (
    <div className="flex items-center justify-center gap-3 py-12 text-slate-500">
      <span className="h-6 w-6 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      <span className="text-sm">{label}</span>
    </div>
  );
}
