import Icon from './Icon.jsx';

export default function EmptyState({ title = 'Nothing here yet', hint, children }) {
  return (
    <div className="flex flex-col items-center gap-2 py-14 text-center">
      <Icon name="box" className="h-10 w-10 text-slate-300" />
      <h2 className="font-medium text-slate-700">{title}</h2>
      {hint && <p className="text-sm text-slate-500">{hint}</p>}
      {children}
    </div>
  );
}
