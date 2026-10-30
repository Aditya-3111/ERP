// ----------------------------------------------------------------------------
// Production module - screens that are plain "list + add/edit form" tables.
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

export const orders = {
  key: "orders",
  title: "Production Orders",
  singular: "Production Order",
  endpoint: "/production/orders/",
  search: true,
  columns: [
    { key: "order_no", label: "Order No" },
    { key: "order_date", label: "Order date", type: "date" },
    { key: "bom_name", label: "BOM" },
    { key: "finished_item_name", label: "Finished item" },
    { key: "planned_quantity", label: "Planned quantity", type: "number" },
    { key: "produced_quantity", label: "Produced quantity", type: "number" },
  ],
  fields: [
    { name: "order_no", label: "Order No", type: "text", required: true, maxLength: 100 },
    { name: "order_date", label: "Order date", type: "date", required: true },
    { name: "bom", label: "BOM", type: "relation", lookup: "bomHeaders", required: true },
    { name: "finished_item", label: "Finished item", type: "relation", lookup: "items", required: true },
    { name: "planned_quantity", label: "Planned quantity", type: "number", step: 0.01, required: true },
    { name: "produced_quantity", label: "Produced quantity", type: "number", step: 0.01 },
    { name: "rejected_quantity", label: "Rejected quantity", type: "number", step: 0.01 },
    { name: "uom", label: "UOM", type: "text", maxLength: 50 },
    { name: "target_godown", label: "Target godown", type: "text", maxLength: 100 },
    { name: "planned_start_date", label: "Planned start date", type: "date" },
    { name: "planned_end_date", label: "Planned end date", type: "date" },
    { name: "actual_start_date", label: "Actual start date", type: "date" },
    { name: "actual_end_date", label: "Actual end date", type: "date" },
    { name: "priority", label: "Priority", type: "select", options: ["low", "medium", "high", "urgent"], default: "medium" },
    { name: "status", label: "Status", type: "select", options: ["planned", "released", "in_progress", "completed", "cancelled", "on_hold"], default: "planned" },
    { name: "sales_order_ref", label: "Sales order ref", type: "text", maxLength: 100 },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["status", "priority"],
};

export const bomHeaders = {
  key: "bom-headers",
  title: "Bills of Material",
  singular: "Bill of Material",
  endpoint: "/production/bom-headers/",
  search: true,
  columns: [
    { key: "bom_no", label: "BOM No" },
    { key: "bom_name", label: "BOM name" },
    { key: "finished_item_name", label: "Finished item" },
    { key: "finished_quantity", label: "Finished quantity", type: "number" },
    { key: "finished_uom", label: "Finished UOM" },
    { key: "bom_type", label: "BOM type", type: "badge" },
  ],
  fields: [
    { name: "bom_no", label: "BOM No", type: "text", required: true, maxLength: 100 },
    { name: "bom_name", label: "BOM name", type: "text", required: true, maxLength: 200 },
    { name: "finished_item", label: "Finished item", type: "relation", lookup: "items", required: true },
    { name: "finished_quantity", label: "Finished quantity", type: "number", step: 0.01, default: 1 },
    { name: "finished_uom", label: "Finished UOM", type: "text", default: "Nos", maxLength: 50 },
    { name: "bom_type", label: "BOM type", type: "select", options: ["manufacturing", "assembly", "packing", "subcontract"], default: "manufacturing" },
    { name: "version", label: "Version", type: "text", default: "1.0", maxLength: 20 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
    { name: "is_default", label: "Is default", type: "checkbox" },
    { name: "effective_from", label: "Effective from", type: "date" },
    { name: "effective_to", label: "Effective to", type: "date" },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["bom_type"],
};

export const bomItems = {
  key: "bom-items",
  title: "BOM Items",
  singular: "BOM Item",
  endpoint: "/production/bom-items/",
  search: true,
  columns: [
    { key: "bom_name", label: "BOM" },
    { key: "item_name", label: "Item" },
    { key: "required_quantity", label: "Required quantity", type: "number" },
    { key: "uom", label: "UOM" },
    { key: "scrap_percent", label: "Scrap percent", type: "number" },
    { key: "operation_sequence", label: "Operation sequence" },
  ],
  fields: [
    { name: "bom", label: "BOM", type: "relation", lookup: "bomHeaders", required: true },
    { name: "item", label: "Item", type: "relation", lookup: "items", required: true },
    { name: "required_quantity", label: "Required quantity", type: "number", step: 0.01, required: true },
    { name: "uom", label: "UOM", type: "text", maxLength: 50 },
    { name: "scrap_percent", label: "Scrap percent", type: "number", step: 0.01 },
    { name: "operation_sequence", label: "Operation sequence", type: "number", step: 1 },
    { name: "is_critical", label: "Is critical", type: "checkbox" },
    { name: "cost_per_unit", label: "Cost per unit", type: "number", step: 0.01 },
    { name: "total_cost", label: "Total cost", type: "number", step: 0.01 },
  ],
};

export const outputs = {
  key: "outputs",
  title: "Production Output",
  singular: "Output",
  endpoint: "/production/outputs/",
  search: true,
  columns: [
    { key: "output_no", label: "Output No" },
    { key: "output_date", label: "Output date", type: "date" },
    { key: "item_name", label: "Item" },
    { key: "produced_quantity", label: "Produced quantity", type: "number" },
    { key: "accepted_quantity", label: "Accepted quantity", type: "number" },
    { key: "rejected_quantity", label: "Rejected quantity", type: "number" },
  ],
  fields: [
    { name: "output_no", label: "Output No", type: "text", required: true, maxLength: 100 },
    { name: "output_date", label: "Output date", type: "date", required: true },
    { name: "order", label: "Order", type: "relation", lookup: "productionOrders", required: true },
    { name: "item", label: "Item", type: "relation", lookup: "items", required: true },
    { name: "item_name", label: "Item name", type: "text", required: true, maxLength: 200 },
    { name: "produced_quantity", label: "Produced quantity", type: "number", step: 0.01, required: true },
    { name: "accepted_quantity", label: "Accepted quantity", type: "number", step: 0.01 },
    { name: "rejected_quantity", label: "Rejected quantity", type: "number", step: 0.01 },
    { name: "uom", label: "UOM", type: "text", maxLength: 50 },
    { name: "godown", label: "Godown", type: "relation", lookup: "godowns" },
    { name: "batch_no", label: "Batch No", type: "text", maxLength: 100 },
    { name: "cost_per_unit", label: "Cost per unit", type: "number", step: 0.01 },
    { name: "total_cost", label: "Total cost", type: "number", step: 0.01 },
    { name: "status", label: "Status", type: "text", default: "pending", maxLength: 20 },
    { name: "inspected_by", label: "Inspected by", type: "text", maxLength: 100 },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
};

export const workCenters = {
  key: "work-centers",
  title: "Work Centers",
  singular: "Work Center",
  endpoint: "/production/work-centers/",
  search: true,
  columns: [
    { key: "work_center_code", label: "Work center code" },
    { key: "work_center_name", label: "Work center name" },
    { key: "department", label: "Department" },
    { key: "location", label: "Location" },
    { key: "supervisor", label: "Supervisor" },
    { key: "capacity_per_day", label: "Capacity per day", type: "number" },
  ],
  fields: [
    { name: "work_center_code", label: "Work center code", type: "text", required: true, maxLength: 50 },
    { name: "work_center_name", label: "Work center name", type: "text", required: true, maxLength: 200 },
    { name: "department", label: "Department", type: "text", maxLength: 100 },
    { name: "location", label: "Location", type: "text", maxLength: 200 },
    { name: "supervisor", label: "Supervisor", type: "text", maxLength: 100 },
    { name: "capacity_per_day", label: "Capacity per day", type: "number", step: 0.01 },
    { name: "capacity_uom", label: "Capacity UOM", type: "text", default: "Hours", maxLength: 50 },
    { name: "cost_per_hour", label: "Cost per hour", type: "number", step: 0.01 },
    { name: "overhead_percent", label: "Overhead percent", type: "number", step: 0.01 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const machines = {
  key: "machines",
  title: "Machines",
  singular: "Machine",
  endpoint: "/production/machines/",
  search: true,
  columns: [
    { key: "machine_code", label: "Machine code" },
    { key: "machine_name", label: "Machine name" },
    { key: "work_center_name", label: "Work center" },
    { key: "machine_type", label: "Machine type" },
    { key: "capacity_per_hour", label: "Capacity per hour", type: "number" },
    { key: "power_consumption", label: "Power consumption", type: "number" },
  ],
  fields: [
    { name: "machine_code", label: "Machine code", type: "text", required: true, maxLength: 50 },
    { name: "machine_name", label: "Machine name", type: "text", required: true, maxLength: 200 },
    { name: "work_center", label: "Work center", type: "relation", lookup: "workCenters" },
    { name: "machine_type", label: "Machine type", type: "text", maxLength: 100 },
    { name: "capacity_per_hour", label: "Capacity per hour", type: "number", step: 0.01 },
    { name: "power_consumption", label: "Power consumption", type: "number", step: 0.01 },
    { name: "last_maintenance_date", label: "Last maintenance date", type: "date" },
    { name: "next_maintenance_date", label: "Next maintenance date", type: "date" },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const operations = {
  key: "operations",
  title: "Operations",
  singular: "Operation",
  endpoint: "/production/operations/",
  search: true,
  columns: [
    { key: "operation_code", label: "Operation code" },
    { key: "operation_name", label: "Operation name" },
    { key: "work_center_name", label: "Work center" },
    { key: "setup_time_minutes", label: "Setup time minutes", type: "number" },
    { key: "standard_time_minutes", label: "Standard time minutes", type: "number" },
    { key: "cost_per_operation", label: "Cost per operation", type: "money" },
  ],
  fields: [
    { name: "operation_code", label: "Operation code", type: "text", required: true, maxLength: 50 },
    { name: "operation_name", label: "Operation name", type: "text", required: true, maxLength: 200 },
    { name: "work_center", label: "Work center", type: "relation", lookup: "workCenters" },
    { name: "setup_time_minutes", label: "Setup time minutes", type: "number", step: 0.01 },
    { name: "standard_time_minutes", label: "Standard time minutes", type: "number", step: 0.01 },
    { name: "cost_per_operation", label: "Cost per operation", type: "number", step: 0.01 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const qualityInspections = {
  key: "quality-inspections",
  title: "Quality Inspections",
  singular: "Inspection",
  endpoint: "/production/quality-inspections/",
  search: true,
  columns: [
    { key: "inspection_no", label: "Inspection No" },
    { key: "inspection_date", label: "Inspection date", type: "date" },
    { key: "item_name", label: "Item" },
    { key: "total_quantity", label: "Total quantity", type: "number" },
    { key: "accepted_quantity", label: "Accepted quantity", type: "number" },
    { key: "rejected_quantity", label: "Rejected quantity", type: "number" },
  ],
  fields: [
    { name: "inspection_no", label: "Inspection No", type: "text", required: true, maxLength: 100 },
    { name: "inspection_date", label: "Inspection date", type: "date", required: true },
    { name: "output", label: "Output", type: "relation", lookup: "productionOutputs" },
    { name: "order", label: "Order", type: "relation", lookup: "productionOrders" },
    { name: "item", label: "Item", type: "relation", lookup: "items" },
    { name: "item_name", label: "Item name", type: "text", maxLength: 200 },
    { name: "total_quantity", label: "Total quantity", type: "number", step: 0.01 },
    { name: "accepted_quantity", label: "Accepted quantity", type: "number", step: 0.01 },
    { name: "rejected_quantity", label: "Rejected quantity", type: "number", step: 0.01 },
    { name: "rework_quantity", label: "Rework quantity", type: "number", step: 0.01 },
    { name: "rejection_reason", label: "Rejection reason", type: "text", maxLength: 255 },
    { name: "inspection_result", label: "Inspection result", type: "text", default: "passed", maxLength: 20 },
    { name: "inspected_by", label: "Inspected by", type: "text", maxLength: 100 },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
};

export const resources = [orders, bomHeaders, bomItems, outputs, workCenters, machines, operations, qualityInspections];
