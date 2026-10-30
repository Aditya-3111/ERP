// ----------------------------------------------------------------------------
// Maintenance module - screens that are plain "list + add/edit form" tables.
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

export const assets = {
  key: "assets",
  title: "Assets",
  singular: "Asset",
  endpoint: "/maintenance/assets/",
  search: true,
  columns: [
    { key: "asset_code", label: "Asset code" },
    { key: "asset_name", label: "Asset name" },
    { key: "category_name", label: "Category" },
    { key: "criticality", label: "Criticality", type: "badge" },
    { key: "status", label: "Status", type: "badge" },
    { key: "location", label: "Location" },
  ],
  fields: [
    { name: "asset_code", label: "Asset code", type: "text", required: true, maxLength: 50 },
    { name: "asset_name", label: "Asset name", type: "text", required: true, maxLength: 200 },
    { name: "category", label: "Category", type: "relation", lookup: "assetCategories" },
    { name: "asset_type", label: "Asset type", type: "text", default: "machine", maxLength: 20 },
    { name: "model_no", label: "Model No", type: "text", maxLength: 100 },
    { name: "serial_no", label: "Serial No", type: "text", maxLength: 100 },
    { name: "manufacturer", label: "Manufacturer", type: "text", maxLength: 200 },
    { name: "supplier", label: "Supplier", type: "text", maxLength: 200 },
    { name: "purchase_date", label: "Purchase date", type: "date" },
    { name: "purchase_price", label: "Purchase price", type: "number", step: 0.01 },
    { name: "warranty_start", label: "Warranty start", type: "date" },
    { name: "warranty_end", label: "Warranty end", type: "date" },
    { name: "location", label: "Location", type: "text", maxLength: 200 },
    { name: "department", label: "Department", type: "text", maxLength: 100 },
    { name: "responsible_person", label: "Responsible person", type: "text", maxLength: 100 },
    { name: "criticality", label: "Criticality", type: "select", options: ["critical", "high", "medium", "low"], default: "medium" },
    { name: "status", label: "Status", type: "select", options: ["active", "inactive", "under_maintenance", "scrapped", "sold", "idle"], default: "active" },
    { name: "barcode", label: "Barcode", type: "text", maxLength: 100 },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["status", "criticality"],
};

export const assetCategories = {
  key: "asset-categories",
  title: "Asset Categories",
  singular: "Asset Category",
  endpoint: "/maintenance/asset-categories/",
  search: true,
  columns: [
    { key: "category_name", label: "Category name" },
    { key: "category_code", label: "Category code" },
    { key: "depreciation_rate", label: "Depreciation rate", type: "number" },
    { key: "depreciation_method", label: "Depreciation method" },
    { key: "useful_life_years", label: "Useful life years" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "category_name", label: "Category name", type: "text", required: true, maxLength: 200 },
    { name: "category_code", label: "Category code", type: "text", required: true, maxLength: 50 },
    { name: "parent", label: "Parent", type: "relation", lookup: "assetCategories" },
    { name: "depreciation_rate", label: "Depreciation rate", type: "number", step: 0.01 },
    { name: "depreciation_method", label: "Depreciation method", type: "text", default: "SLM", maxLength: 10 },
    { name: "useful_life_years", label: "Useful life years", type: "number", step: 1, default: 5 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const workOrders = {
  key: "work-orders",
  title: "Work Orders",
  singular: "Work Order",
  endpoint: "/maintenance/work-orders/",
  search: true,
  columns: [
    { key: "wo_no", label: "WO No" },
    { key: "wo_date", label: "WO date", type: "date" },
    { key: "asset_name", label: "Asset" },
    { key: "priority", label: "Priority", type: "badge" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "wo_no", label: "WO No", type: "text", required: true, maxLength: 100 },
    { name: "wo_date", label: "WO date", type: "date", required: true },
    { name: "wo_type", label: "WO type", type: "text", default: "preventive", maxLength: 20 },
    { name: "schedule", label: "Schedule", type: "relation", lookup: "schedules" },
    { name: "asset", label: "Asset", type: "relation", lookup: "assets", required: true },
    { name: "problem_description", label: "Problem description", type: "textarea" },
    { name: "priority", label: "Priority", type: "select", options: ["low", "medium", "high", "critical", "emergency"], default: "medium" },
    { name: "status", label: "Status", type: "select", options: ["open", "assigned", "in_progress", "on_hold", "completed", "cancelled", "closed"], default: "open" },
    { name: "assigned_technician", label: "Assigned technician", type: "text", maxLength: 100 },
    { name: "assigned_team", label: "Assigned team", type: "text", maxLength: 200 },
    { name: "planned_start", label: "Planned start", type: "datetime" },
    { name: "planned_end", label: "Planned end", type: "datetime" },
    { name: "actual_start", label: "Actual start", type: "datetime" },
    { name: "actual_end", label: "Actual end", type: "datetime" },
    { name: "downtime_hours", label: "Downtime hours", type: "number", step: 0.01 },
    { name: "estimated_cost", label: "Estimated cost", type: "number", step: 0.01 },
    { name: "actual_cost", label: "Actual cost", type: "number", step: 0.01 },
    { name: "completion_notes", label: "Completion notes", type: "textarea" },
    { name: "root_cause", label: "Root cause", type: "textarea" },
    { name: "corrective_action", label: "Corrective action", type: "textarea" },
  ],
  filters: ["status", "priority"],
};

export const breakdowns = {
  key: "breakdowns",
  title: "Breakdowns",
  singular: "Breakdown",
  endpoint: "/maintenance/breakdowns/",
  search: true,
  columns: [
    { key: "breakdown_no", label: "Breakdown No" },
    { key: "breakdown_date", label: "Breakdown date", type: "datetime" },
    { key: "asset_name", label: "Asset" },
    { key: "severity", label: "Severity" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "breakdown_no", label: "Breakdown No", type: "text", required: true, maxLength: 100 },
    { name: "breakdown_date", label: "Breakdown date", type: "datetime", required: true },
    { name: "reported_by", label: "Reported by", type: "text", maxLength: 100 },
    { name: "problem_description", label: "Problem description", type: "textarea", required: true },
    { name: "breakdown_type", label: "Breakdown type", type: "text", default: "mechanical", maxLength: 20 },
    { name: "severity", label: "Severity", type: "text", default: "major", maxLength: 20 },
    { name: "downtime_start", label: "Downtime start", type: "datetime" },
    { name: "downtime_end", label: "Downtime end", type: "datetime" },
    { name: "total_downtime_hours", label: "Total downtime hours", type: "number", step: 0.01 },
    { name: "production_loss", label: "Production loss", type: "number", step: 0.01 },
    { name: "root_cause", label: "Root cause", type: "textarea" },
    { name: "corrective_action", label: "Corrective action", type: "textarea" },
    { name: "preventive_action", label: "Preventive action", type: "text" },
    { name: "status", label: "Status", type: "select", options: ["reported", "investigating", "repairing", "resolved", "closed"], default: "reported" },
    { name: "resolved_by", label: "Resolved by", type: "text", maxLength: 100 },
    { name: "resolved_at", label: "Resolved at", type: "datetime" },
    { name: "asset", label: "Asset", type: "relation", lookup: "assets", required: true },
    { name: "work_order", label: "Work order", type: "relation", lookup: "workOrders" },
  ],
  filters: ["status"],
};

export const schedules = {
  key: "schedules",
  title: "Maintenance Schedules",
  singular: "Schedule",
  endpoint: "/maintenance/schedules/",
  search: true,
  columns: [
    { key: "schedule_name", label: "Schedule name" },
    { key: "schedule_code", label: "Schedule code" },
    { key: "asset_name", label: "Asset" },
    { key: "frequency_type", label: "Frequency type", type: "badge" },
    { key: "frequency_value", label: "Frequency value" },
    { key: "last_performed_date", label: "Last performed date", type: "date" },
  ],
  fields: [
    { name: "schedule_name", label: "Schedule name", type: "text", required: true, maxLength: 200 },
    { name: "schedule_code", label: "Schedule code", type: "text", required: true, maxLength: 50 },
    { name: "asset", label: "Asset", type: "relation", lookup: "assets", required: true },
    { name: "frequency_type", label: "Frequency type", type: "select", options: ["daily", "weekly", "biweekly", "monthly", "quarterly", "half_yearly", "yearly", "meter_based", "custom"], default: "monthly" },
    { name: "frequency_value", label: "Frequency value", type: "number", step: 1, default: 1 },
    { name: "last_performed_date", label: "Last performed date", type: "date" },
    { name: "next_due_date", label: "Next due date", type: "date" },
    { name: "estimated_duration_hours", label: "Estimated duration hours", type: "number", step: 0.01 },
    { name: "estimated_cost", label: "Estimated cost", type: "number", step: 0.01 },
    { name: "assigned_technician", label: "Assigned technician", type: "text", maxLength: 100 },
    { name: "priority", label: "Priority", type: "text", default: "medium", maxLength: 10 },
    { name: "status", label: "Status", type: "select", options: ["active", "paused", "completed", "cancelled"], default: "active" },
    { name: "start_date", label: "Start date", type: "date" },
    { name: "end_date", label: "End date", type: "date" },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["frequency_type", "status"],
};

export const tasks = {
  key: "tasks",
  title: "Work Order Tasks",
  singular: "Task",
  endpoint: "/maintenance/tasks/",
  search: true,
  columns: [
    { key: "sequence_no", label: "Sequence No" },
    { key: "check_type", label: "Check type" },
    { key: "expected_value", label: "Expected value" },
    { key: "actual_value", label: "Actual value" },
    { key: "is_completed", label: "Is completed", type: "bool" },
    { key: "completed_by", label: "Completed by" },
  ],
  fields: [
    { name: "work_order", label: "Work order", type: "relation", lookup: "workOrders", required: true },
    { name: "task_description", label: "Task description", type: "textarea", required: true, maxLength: 200 },
    { name: "sequence_no", label: "Sequence No", type: "number", step: 1 },
    { name: "check_type", label: "Check type", type: "text", default: "visual", maxLength: 20 },
    { name: "expected_value", label: "Expected value", type: "text", maxLength: 100 },
    { name: "actual_value", label: "Actual value", type: "text", maxLength: 100 },
    { name: "is_completed", label: "Is completed", type: "checkbox" },
    { name: "completed_by", label: "Completed by", type: "text", maxLength: 100 },
    { name: "completed_at", label: "Completed at", type: "datetime" },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
};

export const resources = [assets, assetCategories, workOrders, breakdowns, schedules, tasks];
