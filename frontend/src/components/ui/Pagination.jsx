import Button from './Button.jsx';

/** "Showing 21-40 of 95"  [Previous] [Next]   (page size is 20, set by the backend) */
export default function Pagination({ page, count, pageSize = 20, onPage }) {
  const pages = Math.max(1, Math.ceil(count / pageSize));
  const first = count === 0 ? 0 : (page - 1) * pageSize + 1;
  const last = Math.min(page * pageSize, count);
  return (
    <div className="flex flex-wrap items-center justify-between gap-2 border-t border-slate-200 px-4 py-3 text-sm text-slate-600">
      <span>Showing {first}-{last} of {count}</span>
      <div className="flex items-center gap-2">
        <Button size="sm" variant="secondary" icon="left" disabled={page <= 1} onClick={() => onPage(page - 1)}>Previous</Button>
        <span>Page {page} / {pages}</span>
        <Button size="sm" variant="secondary" disabled={page >= pages} onClick={() => onPage(page + 1)}>Next</Button>
      </div>
    </div>
  );
}
