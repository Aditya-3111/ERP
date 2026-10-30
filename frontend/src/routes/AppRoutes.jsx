import { Route, Routes } from 'react-router-dom';
import ResourcePage from '../components/crud/ResourcePage.jsx';
import EmptyState from '../components/ui/EmptyState.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { canAccess } from '../modules/access.js';
import { modules } from '../modules/registry.js';
import DashboardPage from '../pages/DashboardPage.jsx';
import LoginPage from '../pages/LoginPage.jsx';
import NotFoundPage from '../pages/NotFoundPage.jsx';
import ProfilePage from '../pages/ProfilePage.jsx';
import ProtectedRoute from './ProtectedRoute.jsx';

/** Shows the page only if the user's role may open that module. */
function ModuleGuard({ moduleKey, children }) {
  const { user } = useAuth();
  if (!canAccess(user, moduleKey)) {
    return <EmptyState title="No access" hint="Your role cannot open this module. Ask an administrator." />;
  }
  return children;
}

/**
 * All URLs of the app.
 *   /login                       sign in
 *   /                            dashboard
 *   /<module>/<table>            auto-generated list page for every resource of a module
 *   /<module>/<custom path>      hand-written pages listed in each module's `routes`
 */
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route index element={<DashboardPage />} />
        <Route path="profile" element={<ProfilePage />} />
        {modules.flatMap((m) => [
          ...(m.routes || []).map((r) => (
            <Route key={`${m.key}/${r.path}`} path={`${m.key}/${r.path}`} element={<ModuleGuard moduleKey={m.key}>{r.element}</ModuleGuard>} />
          )),
          ...m.resources
            .filter((res) => !(m.routes || []).some((r) => r.path === res.key))   // a hand-written page wins
            .map((res) => (
              <Route key={`${m.key}/${res.key}`} path={`${m.key}/${res.key}`}
                element={<ModuleGuard moduleKey={m.key}><ResourcePage key={res.key} resource={res} /></ModuleGuard>} />
            )),
        ])}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
