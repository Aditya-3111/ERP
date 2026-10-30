import { useEffect, useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import { canAccess } from '../../modules/access.js';
import { menuOf, modules } from '../../modules/registry.js';
import Icon from '../ui/Icon.jsx';

const linkClass = ({ isActive }) =>
  `block rounded-md px-3 py-1.5 text-sm ${isActive ? 'bg-brand-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`;

/** Left menu: Dashboard + one expandable group per module the user may open. */
export default function Sidebar({ open, onNavigate }) {
  const { user } = useAuth();
  const { pathname } = useLocation();
  const activeModule = pathname.split('/')[1];
  const [expanded, setExpanded] = useState(activeModule);

  useEffect(() => { setExpanded(activeModule); }, [activeModule]);

  return (
    <aside className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col bg-slate-900 transition-transform lg:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
      <div className="flex h-16 items-center gap-3 border-b border-slate-800 px-5">
        <div className="rounded-lg bg-brand-600 p-2 text-white"><Icon name="scale" className="h-5 w-5" /></div>
        <div>
          <p className="font-bold leading-tight text-white">FinLedger Pro</p>
          <p className="text-xs text-slate-400">Accounting &amp; ERP</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4" aria-label="Main menu">
        <NavLink to="/" end onClick={onNavigate} className={({ isActive }) =>
          `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium ${isActive ? 'bg-brand-600 text-white' : 'text-slate-200 hover:bg-slate-800'}`}>
          <Icon name="dashboard" className="h-4 w-4" /> Dashboard
        </NavLink>

        {modules.filter((m) => canAccess(user, m.key)).map((m) => (
          <div key={m.key}>
            <button type="button" onClick={() => setExpanded(expanded === m.key ? '' : m.key)}
              className={`flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-slate-800 ${activeModule === m.key ? 'text-white' : 'text-slate-200'}`}
              aria-expanded={expanded === m.key}>
              <Icon name={m.icon} className="h-4 w-4" />
              <span className="flex-1 text-left">{m.title}</span>
              <Icon name={expanded === m.key ? 'down' : 'right'} className="h-4 w-4 text-slate-500" />
            </button>
            {expanded === m.key && (
              <ul className="ml-4 mt-1 space-y-0.5 border-l border-slate-700 pl-3">
                {menuOf(m).map((item) => (
                  <li key={item.path}><NavLink to={item.path} onClick={onNavigate} className={linkClass}>{item.label}</NavLink></li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
