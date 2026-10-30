import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import { usePeriod } from '../../context/PeriodContext.jsx';
import Icon from '../ui/Icon.jsx';

/** Top bar: menu button (mobile), financial-year picker, user menu. */
export default function Topbar({ onMenu }) {
  const { user, logout } = useAuth();
  const { years, period, selectYear } = usePeriod();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const name = user?.fullname?.trim() || user?.username || '';

  async function signOut() {
    await logout();
    navigate('/login', { replace: true });
  }

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-slate-200 bg-white px-4">
      <button type="button" className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden" onClick={onMenu} aria-label="Open menu">
        <Icon name="menu" />
      </button>
      <div className="flex-1" />

      <label className="flex items-center gap-2 text-sm text-slate-600">
        <Icon name="calendar" className="h-4 w-4" />
        <select className="input w-auto py-1.5" value={period.guid || ''} onChange={(e) => selectYear(e.target.value)} aria-label="Financial year">
          {years.length === 0 && <option value="">{period.name}</option>}
          {years.map((y) => <option key={y.guid} value={y.guid}>{y.name}</option>)}
        </select>
      </label>

      <div className="relative">
        <button type="button" onClick={() => setOpen(!open)} className="flex items-center gap-2 rounded-lg px-2 py-1.5 hover:bg-slate-100" aria-haspopup="menu" aria-expanded={open}>
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-600 text-sm font-semibold text-white">{name.charAt(0).toUpperCase() || '?'}</span>
          <span className="hidden text-left sm:block">
            <span className="block text-sm font-medium leading-tight text-slate-800" data-testid="user-name">{name}</span>
            <span className="block text-xs text-slate-500">{user?.role_name}</span>
          </span>
        </button>
        {open && (
          <div className="card absolute right-0 mt-2 w-48 p-1" role="menu" onClick={() => setOpen(false)}>
            <Link to="/profile" className="flex items-center gap-2 rounded-md px-3 py-2 text-sm hover:bg-slate-100" role="menuitem"><Icon name="user" className="h-4 w-4" /> My profile</Link>
            <button type="button" onClick={signOut} className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-red-600 hover:bg-red-50" role="menuitem"><Icon name="logout" className="h-4 w-4" /> Sign out</button>
          </div>
        )}
      </div>
    </header>
  );
}
