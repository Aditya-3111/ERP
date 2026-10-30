import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import Alert from '../components/ui/Alert.jsx';
import Button from '../components/ui/Button.jsx';
import Icon from '../components/ui/Icon.jsx';
import { useAuth } from '../context/AuthContext.jsx';

export default function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const from = location.state?.from?.pathname || '/';

  if (user) return <Navigate to={from} replace />;

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError('');
    try {
      await login(username.trim(), password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-brand-700 p-4">
      <div className="card w-full max-w-md p-8">
        <div className="mb-6 flex items-center gap-3">
          <div className="rounded-xl bg-brand-600 p-3 text-white"><Icon name="scale" className="h-6 w-6" /></div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">FinLedger Pro</h1>
            <p className="text-sm text-slate-500">Sign in to continue</p>
          </div>
        </div>
        <form onSubmit={submit} className="space-y-4" noValidate>
          {error && <Alert>{error}</Alert>}
          <div>
            <label htmlFor="username" className="label">Username</label>
            <input id="username" className="input" autoComplete="username" autoFocus value={username} onChange={(e) => setUsername(e.target.value)} />
          </div>
          <div>
            <label htmlFor="password" className="label">Password</label>
            <input id="password" type="password" className="input" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <Button type="submit" className="w-full" loading={busy} disabled={!username || !password}>Sign in</Button>
        </form>
      </div>
    </div>
  );
}
