import { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar.jsx';
import Topbar from './Topbar.jsx';

/** Frame around every logged-in page: sidebar on the left, top bar, then the page itself. */
export default function AppLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  useLocation();   // re-render on navigation
  return (
    <div className="min-h-screen">
      <Sidebar open={menuOpen} onNavigate={() => setMenuOpen(false)} />
      {menuOpen && <div className="fixed inset-0 z-30 bg-slate-900/40 lg:hidden" onClick={() => setMenuOpen(false)} />}
      <div className="lg:pl-64">
        <Topbar onMenu={() => setMenuOpen(true)} />
        <main className="mx-auto max-w-7xl p-4 sm:p-6"><Outlet /></main>
      </div>
    </div>
  );
}
