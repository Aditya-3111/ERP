// Which module each role can see in the menu.
// NOTE: this only hides menu items. The backend itself does not check roles yet
// (every logged-in user can call every API) - see README "Known limitations".
const ROLE_ACCESS = {
  accountant: ['finance'],
  sales: ['crm', 'pos'],
  store: ['inventory'],
  hr: ['hr'],
  gate: ['gate'],
  production: ['production', 'inventory'],
  maintenance: ['maintenance'],
};

export function canAccess(user, moduleKey) {
  if (!user) return false;
  if (user.is_superuser || user.role_code === 'admin') return true;
  if (moduleKey === 'admin') return false;
  return (ROLE_ACCESS[user.role_code] || []).includes(moduleKey);
}
