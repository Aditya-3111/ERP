import { useState } from 'react';
import { api } from '../../api/client.js';
import { clearLookupsFor } from '../../api/lookups.js';
import { useToast } from '../../context/ToastContext.jsx';
import Alert from '../ui/Alert.jsx';
import Button from '../ui/Button.jsx';
import Modal from '../ui/Modal.jsx';
import FormField from './FormField.jsx';
import { allFields, buildBody, initialValues, validate } from './payload.js';

/** Add / edit dialog for any resource.  `row` = null means "add new". */
export default function ResourceForm({ resource, row, onSaved, onClose }) {
  const toast = useToast();
  const fields = allFields(resource);
  const mode = row ? 'edit' : 'create';
  const [values, setValues] = useState(() => initialValues(fields, row));
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const setValue = (name, value) => setValues((v) => ({ ...v, [name]: value }));

  async function submit(e) {
    e.preventDefault();
    const problems = validate(fields, values);
    setErrors(problems);
    setFormError('');
    if (Object.keys(problems).length) { setFormError('Please fill the highlighted fields.'); return; }

    setSaving(true);
    try {
      const body = buildBody(fields, values, mode, row);
      const url = mode === 'edit' ? `${resource.endpoint}${row.guid}/` : resource.endpoint;
      if (mode === 'edit') await api.patch(url, body); else await api.post(url, body);
      clearLookupsFor(resource.endpoint);
      toast.success(`${resource.singular} ${mode === 'edit' ? 'updated' : 'created'}.`);
      onSaved();
    } catch (err) {
      setErrors(err.fieldErrors || {});
      setFormError(err.message);
    } finally {
      setSaving(false);
    }
  }

  const renderFields = (list) => (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      {list.map((f) => <FormField key={f.name} field={f} value={values[f.name]} error={errors[f.name]} onChange={(v) => setValue(f.name, v)} />)}
    </div>
  );

  return (
    <Modal title={`${mode === 'edit' ? 'Edit' : 'Add'} ${resource.singular}`} onClose={onClose} size="xl" footer={
      <>
        <Button variant="secondary" onClick={onClose}>Cancel</Button>
        <Button type="submit" form="resource-form" loading={saving}>Save</Button>
      </>
    }>
      <form id="resource-form" onSubmit={submit} noValidate className="space-y-6">
        {formError && <Alert>{formError}</Alert>}
        {resource.sections
          ? resource.sections.map((s) => (
            <fieldset key={s.title}>
              <legend className="mb-3 text-sm font-semibold text-brand-700">{s.title}</legend>
              {renderFields(s.fields)}
            </fieldset>
          ))
          : renderFields(fields)}
      </form>
    </Modal>
  );
}
