import { useState } from 'react';
import { api } from '../api/client.js';
import Alert from '../components/ui/Alert.jsx';
import Button from '../components/ui/Button.jsx';
import { Card } from '../components/ui/Card.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { useToast } from '../context/ToastContext.jsx';

export default function ProfilePage() {
  const { user } = useAuth();
  const toast = useToast();
  const [form, setForm] = useState({ old_password: '', new_password: '', confirm: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setError('');
    if (form.new_password.length < 6) return setError('New password must have at least 6 characters.');
    if (form.new_password !== form.confirm) return setError('The two new passwords are not the same.');
    setBusy(true);
    try {
      await api.post('/auth/change-password/', { old_password: form.old_password, new_password: form.new_password });
      toast.success('Password changed.');
      setForm({ old_password: '', new_password: '', confirm: '' });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const rows = [['Username', user.username], ['Name', user.fullname || '-'], ['Email', user.email || '-'], ['Role', user.role_name || '-'], ['Mobile', user.mobile || '-']];
  return (
    <>
      <PageHeader title="My profile" />
      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Account">
          <dl className="space-y-3 text-sm">
            {rows.map(([k, v]) => <div key={k} className="flex justify-between border-b border-slate-100 pb-2"><dt className="text-slate-500">{k}</dt><dd className="font-medium text-slate-800">{v}</dd></div>)}
          </dl>
        </Card>
        <Card title="Change password">
          <form onSubmit={submit} className="space-y-4" noValidate>
            {error && <Alert>{error}</Alert>}
            <div><label className="label" htmlFor="old_password">Current password</label><input id="old_password" type="password" className="input" value={form.old_password} onChange={set('old_password')} /></div>
            <div><label className="label" htmlFor="new_password">New password</label><input id="new_password" type="password" className="input" value={form.new_password} onChange={set('new_password')} /></div>
            <div><label className="label" htmlFor="confirm">Repeat new password</label><input id="confirm" type="password" className="input" value={form.confirm} onChange={set('confirm')} /></div>
            <Button type="submit" loading={busy} disabled={!form.old_password}>Change password</Button>
          </form>
        </Card>
      </div>
    </>
  );
}
