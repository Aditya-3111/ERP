// Administration: users, roles, company, settings and the system tables.
import { resources } from './resources.js';

const READ_ONLY = ['audit-logs'];                       // logs are written by the system, never edited by hand

export default {
  key: 'admin',
  title: 'Administration',
  icon: 'admin',
  resources: resources.map((r) => (READ_ONLY.includes(r.key) ? { ...r, readOnly: true } : r)),
  routes: [],
};
