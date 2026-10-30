import { Link } from 'react-router-dom';
import EmptyState from '../components/ui/EmptyState.jsx';

export default function NotFoundPage() {
  return <EmptyState title="Page not found" hint="The address does not exist."><Link to="/" className="btn btn-primary mt-2">Go to dashboard</Link></EmptyState>;
}
