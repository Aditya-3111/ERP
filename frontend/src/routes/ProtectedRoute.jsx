import { Navigate, useLocation } from 'react-router-dom';
import AppLayout from '../components/layout/AppLayout.jsx';
import Spinner from '../components/ui/Spinner.jsx';
import { useAuth } from '../context/AuthContext.jsx';
import { PeriodProvider } from '../context/PeriodContext.jsx';

/** Everything inside needs a login. Not logged in -> /login (and we remember where to come back). */
export default function ProtectedRoute() {
  const { user, loading } = useAuth();
  const location = useLocation();
  if (loading) return <Spinner label="Checking your login..." />;
  if (!user) return <Navigate to="/login" replace state={{ from: location }} />;
  return (
    <PeriodProvider>
      <AppLayout />
    </PeriodProvider>
  );
}
