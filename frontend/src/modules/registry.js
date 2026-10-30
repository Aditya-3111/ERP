// The list of modules shown in the sidebar and turned into routes.
// To add a new module: create modules/<name>/index.jsx and add it to the list below.
import admin from './admin/index.jsx';
import crm from './crm/index.jsx';
import finance from './finance/index.jsx';
import gate from './gate/index.jsx';
import hr from './hr/index.jsx';
import inventory from './inventory/index.jsx';
import maintenance from './maintenance/index.jsx';
import pos from './pos/index.jsx';
import production from './production/index.jsx';

export const modules = [finance, inventory, crm, hr, gate, pos, production, maintenance, admin];

/** Sidebar entries of a module: its own `menu`, or one entry per table. */
export function menuOf(module) {
  return module.menu || module.resources.map((r) => ({ label: r.title, path: `/${module.key}/${r.key}` }));
}
