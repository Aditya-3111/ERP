import useLookup from '../../hooks/useLookup.js';
import { humanize } from '../../utils/format.js';

const INPUT_TYPE = { text: 'text', email: 'email', url: 'url', number: 'number', date: 'date', datetime: 'datetime-local', time: 'time', password: 'password' };

function RelationSelect({ field, value, onChange, className }) {
  const { options, loading, error } = useLookup(field.lookup);
  return (
    <select id={field.name} className={className} value={value} onChange={(e) => onChange(e.target.value)} disabled={loading}>
      <option value="">{loading ? 'Loading...' : error ? 'Could not load list' : '- select -'}</option>
      {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
    </select>
  );
}

/** One label + input.  The input shown depends on field.type (see resources.js). */
export default function FormField({ field, value, onChange, error }) {
  const cls = `input ${error ? 'input-error' : ''}`;
  let control;

  if (field.type === 'textarea') {
    control = <textarea id={field.name} rows={3} className={cls} value={value} maxLength={field.maxLength} onChange={(e) => onChange(e.target.value)} />;
  } else if (field.type === 'select') {
    control = (
      <select id={field.name} className={cls} value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">- select -</option>
        {field.options.map((o) => {
          const v = typeof o === 'object' ? o.value : o;
          const l = typeof o === 'object' ? o.label : humanize(o);
          return <option key={v} value={v}>{l}</option>;
        })}
      </select>
    );
  } else if (field.type === 'relation') {
    control = <RelationSelect field={field} value={value} onChange={onChange} className={cls} />;
  } else if (field.type === 'checkbox') {
    return (
      <div className="flex items-center gap-2 pt-6">
        <input id={field.name} type="checkbox" className="h-4 w-4 rounded border-slate-300 text-brand-600" checked={Boolean(value)} onChange={(e) => onChange(e.target.checked)} />
        <label htmlFor={field.name} className="text-sm text-slate-700">{field.label}</label>
      </div>
    );
  } else if (field.type === 'file') {
    control = <input id={field.name} type="file" className={cls} onChange={(e) => onChange(e.target.files[0] || '')} />;
  } else {
    control = (
      <input id={field.name} type={INPUT_TYPE[field.type] || 'text'} className={cls} value={value}
        step={field.step} maxLength={field.maxLength} autoComplete="off"
        onChange={(e) => onChange(e.target.value)} />
    );
  }

  return (
    <div className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
      <label htmlFor={field.name} className="label">{field.label}{field.required && <span className="text-red-500"> *</span>}</label>
      {control}
      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  );
}
