import { BADGE_CLASSES, badgeTone, humanize } from '../../utils/format.js';

/** Coloured pill for status words: active, pending, cancelled ... */
export default function Badge({ value, tone }) {
  if (value === null || value === undefined || value === '') return <span className="text-slate-400">-</span>;
  return <span className={`badge ${BADGE_CLASSES[tone || badgeTone(value)]}`}>{humanize(value)}</span>;
}
