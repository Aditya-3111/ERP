// Inventory module: stock items, groups, godowns, batches, MRN ...
import { resources } from './resources.js';
import StockMovementsPage from './pages/StockMovementsPage.jsx';

export default {
  key: 'inventory',
  title: 'Inventory',
  icon: 'inventory',
  resources: resources.map((r) => (r.key === 'items'
    ? { ...r, rowActions: [{ label: 'Movements', to: (row) => `/inventory/items/${row.guid}/movements` }] }
    : r)),
  routes: [{ path: 'items/:id/movements', element: <StockMovementsPage /> }],
};
