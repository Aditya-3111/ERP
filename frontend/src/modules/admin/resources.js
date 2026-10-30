// ----------------------------------------------------------------------------
// Administration module - screens that are plain "list + add/edit form" tables.
// One object per table.  The shared <ResourcePage> component turns each object
// into a full page (search, paging, add / edit / delete).  To add a column or a
// form field, just edit the lists below - no other file needs to change.
//
//   endpoint : Django REST URL (relative to VITE_API_URL)
//   columns  : what the table shows        (type: date | money | number | bool | badge)
//   fields   : what the form asks for      (type: text | textarea | number | select | checkbox |
//                                           date | datetime | time | email | url | relation | file)
//   relation : drop-down filled from another table -> see src/api/lookups.js
// ----------------------------------------------------------------------------

export const users = {
  key: "users",
  title: "Users",
  singular: "User",
  endpoint: "/core/users/",
  search: false,
  columns: [
    { key: "username", label: "Username" },
    { key: "first_name", label: "First name" },
    { key: "last_name", label: "Last name" },
    { key: "email", label: "Email" },
    { key: "role_name", label: "Role" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "username", label: "Username", type: "text", required: true, maxLength: 150 },
    { name: "password", label: "Password", type: "password" },
    { name: "email", label: "Email", type: "email" },
    { name: "first_name", label: "First name", type: "text", maxLength: 150 },
    { name: "last_name", label: "Last name", type: "text", maxLength: 150 },
    { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
    { name: "role", label: "Role", type: "relation", lookup: "roles" },
    { name: "status", label: "Status", type: "select", options: ["active", "inactive"] },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const roles = {
  key: "roles",
  title: "Roles",
  singular: "Role",
  endpoint: "/core/roles/",
  search: false,
  columns: [
    { key: "name", label: "Name" },
    { key: "label", label: "Label" },
    { key: "description", label: "Description" },
    { key: "is_system", label: "Is system", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 50 },
    { name: "label", label: "Label", type: "text", required: true, maxLength: 100 },
    { name: "description", label: "Description", type: "textarea" },
    { name: "is_system", label: "Is system", type: "checkbox" },
  ],
};

export const financialYears = {
  key: "financial-years",
  title: "Financial Years",
  singular: "Financial Year",
  endpoint: "/core/financial-years/",
  search: false,
  columns: [
    { key: "name", label: "Name" },
    { key: "start_date", label: "Start date", type: "date" },
    { key: "end_date", label: "End date", type: "date" },
    { key: "is_active", label: "Is active", type: "bool" },
    { key: "is_locked", label: "Is locked", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 50 },
    { name: "start_date", label: "Start date", type: "date", required: true },
    { name: "end_date", label: "End date", type: "date", required: true },
    { name: "is_active", label: "Is active", type: "checkbox" },
    { name: "is_locked", label: "Is locked", type: "checkbox" },
  ],
};

export const companyProfiles = {
  key: "company-profiles",
  title: "Company Profile",
  singular: "Company",
  endpoint: "/core/company-profiles/",
  search: false,
  columns: [
    { key: "company_name", label: "Company name" },
    { key: "legal_name", label: "Legal name" },
    { key: "city", label: "City" },
    { key: "state", label: "State" },
    { key: "pincode", label: "Pincode" },
    { key: "country", label: "Country" },
  ],
  fields: [
    { name: "company_name", label: "Company name", type: "text", required: true, maxLength: 200 },
    { name: "legal_name", label: "Legal name", type: "text", maxLength: 200 },
    { name: "address", label: "Address", type: "textarea" },
    { name: "city", label: "City", type: "text", maxLength: 100 },
    { name: "state", label: "State", type: "text", maxLength: 100 },
    { name: "pincode", label: "Pincode", type: "text", maxLength: 10 },
    { name: "country", label: "Country", type: "text", default: "India", maxLength: 50 },
    { name: "gstin", label: "GSTIN", type: "text", maxLength: 15 },
    { name: "pan", label: "PAN", type: "text", maxLength: 10 },
    { name: "tan", label: "TAN", type: "text", maxLength: 10 },
    { name: "cin", label: "CIN", type: "text", maxLength: 21 },
    { name: "email", label: "Email", type: "email" },
    { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
    { name: "phone", label: "Phone", type: "text", maxLength: 15 },
    { name: "website", label: "Website", type: "url" },
  ],
};

export const branches = {
  key: "branches",
  title: "Branches",
  singular: "Branch",
  endpoint: "/core/branches/",
  search: false,
  columns: [
    { key: "name", label: "Name" },
    { key: "code", label: "Code" },
    { key: "city", label: "City" },
    { key: "state", label: "State" },
    { key: "pincode", label: "Pincode" },
    { key: "gstin", label: "GSTIN" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 100 },
    { name: "code", label: "Code", type: "text", maxLength: 20 },
    { name: "address", label: "Address", type: "textarea" },
    { name: "city", label: "City", type: "text", maxLength: 100 },
    { name: "state", label: "State", type: "text", maxLength: 100 },
    { name: "pincode", label: "Pincode", type: "text", maxLength: 10 },
    { name: "gstin", label: "GSTIN", type: "text", maxLength: 15 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const settings = {
  key: "settings",
  title: "System Settings",
  singular: "Setting",
  endpoint: "/core/settings/",
  search: false,
  columns: [
    { key: "key", label: "Key" },
    { key: "value", label: "Value" },
    { key: "setting_type", label: "Setting type", type: "badge" },
  ],
  fields: [
    { name: "key", label: "Key", type: "text", required: true, maxLength: 100 },
    { name: "value", label: "Value", type: "text", required: true },
    { name: "setting_type", label: "Setting type", type: "select", options: ["text", "number", "boolean", "json"], default: "text" },
    { name: "description", label: "Description", type: "textarea", maxLength: 255 },
  ],
};

export const auditLogs = {
  key: "audit-logs",
  title: "Audit Logs",
  singular: "Audit Log",
  endpoint: "/core/audit-logs/",
  search: false,
  columns: [
    { key: "user_name", label: "User" },
    { key: "action", label: "Action" },
    { key: "module", label: "Module" },
    { key: "ip_address", label: "IP address" },
  ],
  fields: [
    { name: "user", label: "User", type: "relation", lookup: "users" },
    { name: "action", label: "Action", type: "text", required: true, maxLength: 100 },
    { name: "module", label: "Module", type: "text", required: true, maxLength: 100 },
    { name: "details", label: "Details", type: "textarea" },
    { name: "ip_address", label: "IP address", type: "text" },
  ],
};

export const notifications = {
  key: "notifications",
  title: "Notifications",
  singular: "Notification",
  endpoint: "/core/notifications/",
  search: true,
  columns: [
    { key: "notification_type", label: "Notification type", type: "badge" },
    { key: "title", label: "Title" },
    { key: "link", label: "Link" },
    { key: "is_read", label: "Is read", type: "bool" },
    { key: "read_at", label: "Read at", type: "datetime" },
  ],
  fields: [
    { name: "user", label: "User", type: "relation", lookup: "users", required: true },
    { name: "notification_type", label: "Notification type", type: "select", options: ["info", "success", "warning", "error"], default: "info" },
    { name: "title", label: "Title", type: "text", required: true, maxLength: 200 },
    { name: "message", label: "Message", type: "textarea" },
    { name: "link", label: "Link", type: "text", maxLength: 500 },
    { name: "is_read", label: "Is read", type: "checkbox" },
    { name: "read_at", label: "Read at", type: "datetime" },
  ],
  filters: ["notification_type"],
};

export const modules = {
  key: "modules",
  title: "Modules",
  singular: "Module",
  endpoint: "/admin/modules/",
  search: false,
  columns: [
    { key: "module_key", label: "Module key" },
    { key: "module_name", label: "Module name" },
    { key: "module_icon", label: "Module icon" },
    { key: "module_description", label: "Module description" },
    { key: "module_url", label: "Module URL" },
    { key: "parent_module", label: "Parent module" },
  ],
  fields: [
    { name: "module_key", label: "Module key", type: "text", required: true, maxLength: 50 },
    { name: "module_name", label: "Module name", type: "text", required: true, maxLength: 100 },
    { name: "module_icon", label: "Module icon", type: "text", maxLength: 50 },
    { name: "module_description", label: "Module description", type: "text" },
    { name: "module_url", label: "Module URL", type: "text", maxLength: 200 },
    { name: "parent_module", label: "Parent module", type: "text", maxLength: 50 },
    { name: "sort_order", label: "Sort order", type: "number", step: 1 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
    { name: "is_core", label: "Is core", type: "checkbox" },
    { name: "version", label: "Version", type: "text", default: "1.0.0", maxLength: 20 },
  ],
};

export const moduleSettings = {
  key: "module-settings",
  title: "Module Settings",
  singular: "Module Setting",
  endpoint: "/admin/module-settings/",
  search: false,
  columns: [
    { key: "setting_key", label: "Setting key" },
    { key: "setting_value", label: "Setting value" },
    { key: "setting_type", label: "Setting type", type: "badge" },
  ],
  fields: [
    { name: "setting_key", label: "Setting key", type: "text", required: true, maxLength: 100 },
    { name: "setting_value", label: "Setting value", type: "text" },
    { name: "setting_type", label: "Setting type", type: "select", options: ["text", "number", "boolean", "json", "file"], default: "text" },
    { name: "module", label: "Module", type: "relation", lookup: "modules", required: true },
  ],
};

export const menuGroups = {
  key: "menu-groups",
  title: "Menu Groups",
  singular: "Menu Group",
  endpoint: "/admin/menu-groups/",
  search: false,
  columns: [
    { key: "group_key", label: "Group key" },
    { key: "group_label", label: "Group label" },
    { key: "group_icon", label: "Group icon" },
    { key: "sort_order", label: "Sort order" },
    { key: "is_default_open", label: "Is default open", type: "bool" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "group_key", label: "Group key", type: "text", required: true, maxLength: 50 },
    { name: "group_label", label: "Group label", type: "text", required: true, maxLength: 100 },
    { name: "group_icon", label: "Group icon", type: "text", maxLength: 50 },
    { name: "sort_order", label: "Sort order", type: "number", step: 1 },
    { name: "is_default_open", label: "Is default open", type: "checkbox" },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const menuItems = {
  key: "menu-items",
  title: "Menu Items",
  singular: "Menu Item",
  endpoint: "/admin/menu-items/",
  search: false,
  columns: [
    { key: "item_key", label: "Item key" },
    { key: "item_label", label: "Item label" },
    { key: "item_icon", label: "Item icon" },
    { key: "item_page", label: "Item page" },
    { key: "item_url", label: "Item URL" },
    { key: "sort_order", label: "Sort order" },
  ],
  fields: [
    { name: "item_key", label: "Item key", type: "text", required: true, maxLength: 50 },
    { name: "item_label", label: "Item label", type: "text", required: true, maxLength: 100 },
    { name: "item_icon", label: "Item icon", type: "text", maxLength: 50 },
    { name: "item_page", label: "Item page", type: "text", required: true, maxLength: 100 },
    { name: "item_url", label: "Item URL", type: "text", maxLength: 200 },
    { name: "sort_order", label: "Sort order", type: "number", step: 1 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
    { name: "required_permission", label: "Required permission", type: "text", maxLength: 50 },
    { name: "badge_text", label: "Badge text", type: "text", maxLength: 50 },
    { name: "badge_color", label: "Badge color", type: "text", maxLength: 20 },
    { name: "group", label: "Group", type: "relation", lookup: "menuGroups", required: true },
    { name: "parent_item", label: "Parent item", type: "relation", lookup: "menuItems" },
  ],
};

export const permissionGroups = {
  key: "permission-groups",
  title: "Permission Groups",
  singular: "Permission Group",
  endpoint: "/admin/permission-groups/",
  search: false,
  columns: [
    { key: "group_name", label: "Group name" },
    { key: "group_key", label: "Group key" },
  ],
  fields: [
    { name: "group_name", label: "Group name", type: "text", required: true, maxLength: 100 },
    { name: "group_key", label: "Group key", type: "text", required: true, maxLength: 50 },
    { name: "description", label: "Description", type: "textarea" },
  ],
};

export const permissions = {
  key: "permissions",
  title: "Permissions",
  singular: "Permission",
  endpoint: "/admin/permissions/",
  search: false,
  columns: [
    { key: "permission_key", label: "Permission key" },
    { key: "permission_name", label: "Permission name" },
  ],
  fields: [
    { name: "permission_key", label: "Permission key", type: "text", required: true, maxLength: 100 },
    { name: "permission_name", label: "Permission name", type: "text", required: true, maxLength: 200 },
    { name: "description", label: "Description", type: "textarea" },
    { name: "permission_group", label: "Permission group", type: "relation", lookup: "permissionGroups" },
    { name: "module", label: "Module", type: "relation", lookup: "modules" },
  ],
};

export const rolePermissions = {
  key: "role-permissions",
  title: "Role Permissions",
  singular: "Role Permission",
  endpoint: "/admin/role-permissions/",
  search: false,
  columns: [
    { key: "role_name", label: "Role" },
    { key: "permission_name", label: "Permission" },
    { key: "access_level", label: "Access level", type: "badge" },
  ],
  fields: [
    { name: "access_level", label: "Access level", type: "select", options: ["deny", "read", "write", "delete", "full"], default: "read" },
    { name: "role", label: "Role", type: "relation", lookup: "roles", required: true },
    { name: "permission", label: "Permission", type: "relation", lookup: "permissions", required: true },
    { name: "granted_by", label: "Granted by", type: "relation", lookup: "users" },
  ],
};

export const userPermissions = {
  key: "user-permissions",
  title: "User Permissions",
  singular: "User Permission",
  endpoint: "/admin/user-permissions/",
  search: false,
  columns: [
    { key: "permission_name", label: "Permission" },
    { key: "access_level", label: "Access level", type: "badge" },
    { key: "expires_at", label: "Expires at", type: "datetime" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "access_level", label: "Access level", type: "select", options: ["deny", "read", "write", "delete", "full"], default: "read" },
    { name: "expires_at", label: "Expires at", type: "datetime" },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
    { name: "user", label: "User", type: "relation", lookup: "users", required: true },
    { name: "permission", label: "Permission", type: "relation", lookup: "permissions", required: true },
    { name: "granted_by", label: "Granted by", type: "relation", lookup: "users" },
  ],
};

export const themes = {
  key: "themes",
  title: "Themes",
  singular: "Theme",
  endpoint: "/admin/themes/",
  search: false,
  columns: [
    { key: "theme_mode", label: "Theme mode", type: "badge" },
    { key: "primary_color", label: "Primary color" },
    { key: "accent_color", label: "Accent color" },
    { key: "font_size", label: "Font size" },
    { key: "sidebar_collapsed", label: "Sidebar collapsed", type: "bool" },
    { key: "layout_density", label: "Layout density", type: "badge" },
  ],
  fields: [
    { name: "theme_mode", label: "Theme mode", type: "select", options: ["light", "dark", "auto"], default: "light" },
    { name: "primary_color", label: "Primary color", type: "text", default: "#1a237e", maxLength: 20 },
    { name: "accent_color", label: "Accent color", type: "text", default: "#ff6f00", maxLength: 20 },
    { name: "font_size", label: "Font size", type: "text", default: "13px", maxLength: 10 },
    { name: "sidebar_collapsed", label: "Sidebar collapsed", type: "checkbox" },
    { name: "layout_density", label: "Layout density", type: "select", options: ["compact", "comfortable", "spacious"], default: "comfortable" },
    { name: "user", label: "User", type: "relation", lookup: "users", required: true },
  ],
};

export const resources = [users, roles, financialYears, companyProfiles, branches, settings, auditLogs, notifications, modules, moduleSettings, menuGroups, menuItems, permissionGroups, permissions, rolePermissions, userPermissions, themes];
