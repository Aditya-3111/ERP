// ----------------------------------------------------------------------------
// Pure helper functions for forms (no React inside, so they are easy to test).
//   initialValues : API row  ->  values shown in the form inputs
//   validate      : checks required fields before we bother the server
//   buildBody     : form values -> JSON (or FormData when a file was chosen)
// ----------------------------------------------------------------------------
import { toLocalInput } from '../../utils/format.js';

/** All fields of a resource, whether it is written with `fields` or with `sections`. */
export function allFields(resource) {
  return resource.sections ? resource.sections.flatMap((s) => s.fields) : resource.fields || [];
}

export function initialValues(fields, row) {
  const values = {};
  for (const f of fields) {
    // new record: start from the default the database would use (e.g. "Is active" = ticked)
    const raw = row ? row[f.name] : f.default;
    if (f.type === 'checkbox') values[f.name] = Boolean(raw);
    else if (f.type === 'datetime') values[f.name] = toLocalInput(raw);
    else if (f.type === 'time') values[f.name] = raw ? String(raw).slice(0, 5) : '';
    else if (f.type === 'file' || f.type === 'password') values[f.name] = '';
    else values[f.name] = raw === null || raw === undefined ? '' : raw;
  }
  return values;
}

const isEmpty = (v) => v === '' || v === null || v === undefined;

export function validate(fields, values) {
  const errors = {};
  for (const f of fields) {
    if (f.required && f.type !== 'checkbox' && isEmpty(values[f.name])) errors[f.name] = 'This field is required.';
  }
  return errors;
}

const TEXT_TYPES = ['text', 'textarea', 'email', 'url'];
const CLEARABLE = ['date', 'datetime', 'time', 'relation'];

/**
 * @param mode      'create' | 'edit'
 * @param original  the row being edited (to know whether an emptied field must be cleared)
 */
export function buildBody(fields, values, mode, original) {
  const payload = {};
  const files = {};
  for (const f of fields) {
    const v = values[f.name];
    if (f.type === 'checkbox') { payload[f.name] = Boolean(v); continue; }
    if (f.type === 'file') { if (typeof File !== 'undefined' && v instanceof File) files[f.name] = v; continue; }
    if (isEmpty(v)) {
      const had = original && !isEmpty(original[f.name]);
      if (mode === 'edit' && had && TEXT_TYPES.includes(f.type)) payload[f.name] = '';
      else if (mode === 'edit' && had && CLEARABLE.includes(f.type)) payload[f.name] = null;
      continue;                                        // otherwise leave it out: the server uses its default
    }
    if (f.type === 'number') payload[f.name] = Number(v);
    else if (f.type === 'datetime') payload[f.name] = new Date(v).toISOString();
    else payload[f.name] = v;
  }
  if (Object.keys(files).length === 0) return payload;

  const form = new FormData();                          // a file can only travel as multipart form data
  Object.entries(payload).forEach(([k, v]) => v !== null && form.append(k, v));
  Object.entries(files).forEach(([k, file]) => form.append(k, file));
  return form;
}
