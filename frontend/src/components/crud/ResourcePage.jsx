import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, rowsOf } from '../../api/client.js';
import { clearLookupsFor } from '../../api/lookups.js';
import { useToast } from '../../context/ToastContext.jsx';
import useDebounce from '../../hooks/useDebounce.js';
import { humanize } from '../../utils/format.js';
import Alert from '../ui/Alert.jsx';
import Button from '../ui/Button.jsx';
import { Card } from '../ui/Card.jsx';
import ConfirmDialog from '../ui/ConfirmDialog.jsx';
import EmptyState from '../ui/EmptyState.jsx';
import Icon from '../ui/Icon.jsx';
import PageHeader from '../ui/PageHeader.jsx';
import Pagination from '../ui/Pagination.jsx';
import Spinner from '../ui/Spinner.jsx';
import DataTable from './DataTable.jsx';
import ResourceForm from './ResourceForm.jsx';
import { allFields } from './payload.js';

const PAGE_SIZE = 20;

/**
 * A complete "list + add / edit / delete" page built from a resource config
 * (see modules/<name>/resources.js).  Most screens of the app are just this component.
 *
 * Optional config keys:  readOnly (no add/edit/delete),  rowActions: [{label, to(row)}]
 */
export default function ResourcePage({ resource }) {
  const toast = useToast();
  const [page, setPage] = useState(1);
  const [searchText, setSearchText] = useState('');
  const search = useDebounce(searchText);
  const [filterValues, setFilterValues] = useState({});
  const [state, setState] = useState({ rows: [], count: 0, loading: true, error: null });
  const [editing, setEditing] = useState(null);       // null = closed, {} = add, row = edit
  const [deleting, setDeleting] = useState(null);
  const [deleteBusy, setDeleteBusy] = useState(false);

  const fields = allFields(resource);
  const filterFields = (resource.filters || []).map((name) => fields.find((f) => f.name === name)).filter(Boolean);

  // a different table was opened (same component, new config): start from page 1
  useEffect(() => { setPage(1); setSearchText(''); setFilterValues((v) => (Object.keys(v).length ? {} : v)); }, [resource.key]);

  const load = useCallback(() => {
    setState((s) => ({ ...s, loading: true, error: null }));
    api.get(resource.endpoint, { page, search, ...filterValues })
      .then((data) => setState({ rows: rowsOf(data), count: data.count ?? rowsOf(data).length, loading: false, error: null }))
      .catch((error) => setState({ rows: [], count: 0, loading: false, error }));
  }, [resource.endpoint, page, search, filterValues]);

  useEffect(() => { load(); }, [load]);
  useEffect(() => { setPage(1); }, [search, filterValues]);

  async function confirmDelete() {
    setDeleteBusy(true);
    try {
      await api.delete(`${resource.endpoint}${deleting.guid}/`);
      clearLookupsFor(resource.endpoint);
      toast.success(`${resource.singular} deleted.`);
      setDeleting(null);
      load();
    } catch (err) {
      toast.error(err.message);
      setDeleting(null);
    } finally {
      setDeleteBusy(false);
    }
  }

  const actions = (row) => (
    <div className="flex justify-end gap-1">
      {(resource.rowActions || []).map((a) => (
        <Link key={a.label} to={a.to(row)} className="btn btn-ghost btn-sm">{a.label}</Link>
      ))}
      {!resource.readOnly && (
        <>
          <button type="button" className="btn btn-ghost btn-sm" onClick={() => setEditing(row)} aria-label={`Edit ${resource.singular}`}><Icon name="edit" className="h-4 w-4" /></button>
          <button type="button" className="btn btn-ghost btn-sm text-red-600" onClick={() => setDeleting(row)} aria-label={`Delete ${resource.singular}`}><Icon name="trash" className="h-4 w-4" /></button>
        </>
      )}
    </div>
  );

  return (
    <>
      <PageHeader title={resource.title} subtitle={`${state.count} record${state.count === 1 ? '' : 's'}`}>
        {!resource.readOnly && <Button icon="plus" onClick={() => setEditing({})}>Add {resource.singular}</Button>}
      </PageHeader>

      <Card bodyClassName="p-0">
        {(resource.search || filterFields.length > 0) && (
          <div className="flex flex-wrap items-center gap-3 border-b border-slate-200 p-4">
            {resource.search && (
              <div className="relative w-full max-w-xs">
                <Icon name="search" className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                <input className="input pl-9" placeholder={`Search ${resource.title.toLowerCase()}...`} value={searchText} onChange={(e) => setSearchText(e.target.value)} aria-label="Search" />
              </div>
            )}
            {filterFields.map((f) => (
              <select key={f.name} className="input w-auto" aria-label={f.label} value={filterValues[f.name] || ''}
                onChange={(e) => setFilterValues((v) => ({ ...v, [f.name]: e.target.value }))}>
                <option value="">All {f.label.toLowerCase()}</option>
                {f.options.map((o) => <option key={o} value={o}>{humanize(o)}</option>)}
              </select>
            ))}
          </div>
        )}

        {state.error && <div className="p-4"><Alert onRetry={load}>{state.error.message}</Alert></div>}
        {state.loading && <Spinner />}
        {!state.loading && !state.error && state.rows.length === 0 && (
          <EmptyState title={`No ${resource.title.toLowerCase()} found`} hint={search ? 'Try a different search.' : resource.readOnly ? '' : `Click "Add ${resource.singular}" to create the first one.`} />
        )}
        {!state.loading && state.rows.length > 0 && (
          <>
            <DataTable columns={resource.columns} rows={state.rows} actions={actions} />
            <Pagination page={page} count={state.count} pageSize={PAGE_SIZE} onPage={setPage} />
          </>
        )}
      </Card>

      {editing && (
        <ResourceForm resource={resource} row={editing.guid ? editing : null}
          onClose={() => setEditing(null)} onSaved={() => { setEditing(null); load(); }} />
      )}
      {deleting && (
        <ConfirmDialog message={`Delete this ${resource.singular.toLowerCase()}? This cannot be undone.`}
          loading={deleteBusy} onConfirm={confirmDelete} onCancel={() => setDeleting(null)} />
      )}
    </>
  );
}
