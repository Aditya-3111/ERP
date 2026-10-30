// Small formatting helpers used by tables and reports.

export const humanize = (value) => {
  const text = String(value ?? '').replace(/_/g, ' ').trim();
  return text ? text.charAt(0).toUpperCase() + text.slice(1) : '';
};

export function formatMoney(value) {
  const n = Number(value);
  if (value === null || value === undefined || value === '' || Number.isNaN(n)) return '-';
  return '₹ ' + n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

/** Whole rupees, no paise - for small dashboard tiles. */
export function formatMoneyWhole(value) {
  const n = Number(value);
  if (value === null || value === undefined || value === '' || Number.isNaN(n)) return '-';
  return '₹ ' + n.toLocaleString('en-IN', { maximumFractionDigits: 0 });
}

export function formatNumber(value) {
  const n = Number(value);
  if (value === null || value === undefined || value === '' || Number.isNaN(n)) return '-';
  return n.toLocaleString('en-IN', { maximumFractionDigits: 3 });
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** '2026-04-05' -> '05 Apr 2026'   (no timezone surprises: the date is not converted) */
export function formatDate(value) {
  if (!value) return '-';
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(value));
  if (!m) return String(value);
  return `${m[3]} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
}

export function formatDateTime(value) {
  if (!value) return '-';
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return String(value);
  const hh = String(d.getHours()).padStart(2, '0');
  const mm = String(d.getMinutes()).padStart(2, '0');
  return `${String(d.getDate()).padStart(2, '0')} ${MONTHS[d.getMonth()]} ${d.getFullYear()} ${hh}:${mm}`;
}

/** Today as YYYY-MM-DD in the user's own timezone. */
export function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

/** ISO date-time from the API  ->  value for <input type="datetime-local"> */
export function toLocalInput(value) {
  if (!value) return '';
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return '';
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

/** Colour of a status badge, chosen from the word. */
export function badgeTone(value) {
  const v = String(value ?? '').toLowerCase().replace(/[\s-]+/g, '_');
  if (['active', 'completed', 'converted', 'closed', 'resolved', 'present', 'paid', 'approved', 'checked_in', 'received', 'done', 'customer', 'granted'].includes(v)) return 'green';
  if (['open', 'new', 'pending', 'draft', 'in_progress', 'assigned', 'contacted', 'half_day', 'medium', 'planned', 'on_hold', 'both', 'investigating', 'under_maintenance'].includes(v)) return 'amber';
  if (['inactive', 'cancelled', 'lost', 'absent', 'blocked', 'terminated', 'critical', 'high', 'emergency', 'scrapped', 'rejected', 'resigned'].includes(v)) return 'red';
  if (['qualified', 'supplier', 'checked_out', 'low', 'leave', 'holiday'].includes(v)) return 'blue';
  return 'slate';
}

export const BADGE_CLASSES = {
  green: 'bg-emerald-100 text-emerald-700',
  amber: 'bg-amber-100 text-amber-700',
  red: 'bg-red-100 text-red-700',
  blue: 'bg-sky-100 text-sky-700',
  slate: 'bg-slate-100 text-slate-600',
};
