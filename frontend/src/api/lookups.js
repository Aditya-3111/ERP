// ----------------------------------------------------------------------------
// Drop-down lists that are filled from another table (e.g. "Employee" on the
// attendance form).  A field in a resource config says  { type: 'relation', lookup: 'employees' }
// and the entry below tells where to load the choices from.
//   label : text shown in the drop-down ( ${field} is replaced by that row's value )
//   value : which field is saved (default: guid)
// ----------------------------------------------------------------------------
import { api, rowsOf } from './client.js';

export const LOOKUPS = {
  roles: { endpoint: '/core/roles/', label: '${label}' },
  users: { endpoint: '/core/users/', label: '${username}' },
  branches: { endpoint: '/core/branches/', label: '${name}' },
  financialYears: { endpoint: '/core/financial-years/', label: '${name}' },
  ledgers: { endpoint: '/finance/ledgers/', label: '${name}', value: 'name' },   // vouchers store the ledger NAME
  voucherTypes: { endpoint: '/finance/voucher-types/', label: '${name}', value: 'name' },
  employees: { endpoint: '/hr/employees/', label: '${emp_code} - ${name}' },
  departments: { endpoint: '/hr/departments/', label: '${name}' },
  visitors: { endpoint: '/gate/visitors/', label: '${visitor_id} - ${name}' },
  items: { endpoint: '/inventory/items/', label: '${name}' },
  godowns: { endpoint: '/inventory/godowns/', label: '${name}' },
  assetCategories: { endpoint: '/maintenance/asset-categories/', label: '${category_name}' },
  assets: { endpoint: '/maintenance/assets/', label: '${asset_code} - ${asset_name}' },
  workOrders: { endpoint: '/maintenance/work-orders/', label: '${wo_no}' },
  schedules: { endpoint: '/maintenance/schedules/', label: '${schedule_code} - ${schedule_name}' },
  posSales: { endpoint: '/pos/sales/', label: '${invoice_no}' },
  posSessions: { endpoint: '/pos/sessions/', label: '${session_date}' },
  counters: { endpoint: '/pos/counters/', label: '${counter_name}' },
  paymentMethods: { endpoint: '/pos/payment-methods/', label: '${method_name}' },
  priceLists: { endpoint: '/pos/price-lists/', label: '${price_list_name}' },
  bomHeaders: { endpoint: '/production/bom-headers/', label: '${bom_no} - ${bom_name}' },
  workCenters: { endpoint: '/production/work-centers/', label: '${work_center_name}' },
  productionOrders: { endpoint: '/production/orders/', label: '${order_no}' },
  productionOutputs: { endpoint: '/production/outputs/', label: '${output_no}' },
  menuGroups: { endpoint: '/admin/menu-groups/', label: '${group_label}' },
  menuItems: { endpoint: '/admin/menu-items/', label: '${item_label}' },
  modules: { endpoint: '/admin/modules/', label: '${module_name}' },
  permissionGroups: { endpoint: '/admin/permission-groups/', label: '${group_name}' },
  permissions: { endpoint: '/admin/permissions/', label: '${permission_name}' },
};

/** '${emp_code} - ${name}' + row  ->  'EMP001 - Amit' */
export function fillTemplate(template, row) {
  return template.replace(/\$\{(\w+)\}/g, (_, key) => (row[key] ?? ''));
}

const cache = new Map();   // lookup name -> Promise of [{value, label}]

export function loadLookup(name) {
  const cfg = LOOKUPS[name];
  if (!cfg) return Promise.reject(new Error(`Unknown lookup "${name}"`));
  if (!cache.has(name)) {
    const promise = api.get(cfg.endpoint, { page_size: 500 })
      .then((data) => rowsOf(data).map((row) => ({
        value: row[cfg.value || 'guid'],
        label: fillTemplate(cfg.label, row),
      })))
      .catch((err) => { cache.delete(name); throw err; });
    cache.set(name, promise);
  }
  return cache.get(name);
}

/** Call after a record is created / edited / deleted so drop-downs show the change. */
export function clearLookupsFor(endpoint) {
  for (const [name, cfg] of Object.entries(LOOKUPS)) {
    if (cfg.endpoint === endpoint) cache.delete(name);
  }
}
