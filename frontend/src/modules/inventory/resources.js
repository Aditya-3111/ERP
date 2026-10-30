// ----------------------------------------------------------------------------
// Inventory module - screens that are plain "list + add/edit form" tables.
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

export const stockItems = {
  key: "items",
  title: "Stock Items",
  singular: "Stock Item",
  endpoint: "/inventory/items/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
    { key: "uom", label: "UOM" },
    { key: "closing_balance", label: "Closing balance", type: "money" },
    { key: "min_stock", label: "Min stock", type: "number" },
    { key: "gst_rate", label: "GST rate", type: "number" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  sections: [
    { title: "Basic", fields: [
      { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
      { name: "parent", label: "Parent", type: "text", maxLength: 200 },
      { name: "category", label: "Category", type: "text", maxLength: 200 },
      { name: "alias", label: "Alias", type: "text", maxLength: 100 },
      { name: "part_number", label: "Part number", type: "text", maxLength: 100 },
      { name: "uom", label: "UOM", type: "text", maxLength: 50 },
      { name: "alternate_uom", label: "Alternate UOM", type: "text", maxLength: 50 },
      { name: "conversion", label: "Conversion", type: "number", step: 0.01, default: 1 },
      { name: "description", label: "Description", type: "textarea" },
      { name: "is_active", label: "Is active", type: "checkbox", default: true },
    ] },
    { title: "Stock", fields: [
      { name: "opening_balance", label: "Opening balance", type: "number", step: 0.01 },
      { name: "opening_rate", label: "Opening rate", type: "number", step: 0.01 },
      { name: "opening_value", label: "Opening value", type: "number", step: 0.01 },
      { name: "costing_method", label: "Costing method", type: "select", options: ["FIFO", "LIFO", "Average"], default: "FIFO" },
      { name: "default_godown", label: "Default godown", type: "text", maxLength: 100 },
      { name: "min_stock", label: "Min stock", type: "number", step: 0.01, default: 10 },
      { name: "max_stock", label: "Max stock", type: "number", step: 0.01, default: 1000 },
    ] },
    { title: "GST", fields: [
      { name: "gst_hsn_code", label: "GST HSN code", type: "text", maxLength: 20 },
      { name: "gst_hsn_description", label: "GST HSN description", type: "text", maxLength: 255 },
      { name: "gst_rate", label: "GST rate", type: "number", step: 0.01 },
      { name: "gst_type_of_supply", label: "GST type of supply", type: "text", maxLength: 50 },
      { name: "gst_taxability", label: "GST taxability", type: "text", maxLength: 50 },
    ] },
  ],
};

export const groups = {
  key: "groups",
  title: "Stock Groups",
  singular: "Stock Group",
  endpoint: "/inventory/groups/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
    { name: "parent", label: "Parent", type: "text", maxLength: 200 },
  ],
};

export const categories = {
  key: "categories",
  title: "Stock Categories",
  singular: "Stock Category",
  endpoint: "/inventory/categories/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
    { name: "parent", label: "Parent", type: "text", maxLength: 200 },
  ],
};

export const units = {
  key: "units",
  title: "Units of Measure",
  singular: "Unit",
  endpoint: "/inventory/units/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "formal_name", label: "Formal name" },
    { key: "is_simple_unit", label: "Is simple unit", type: "bool" },
    { key: "base_units", label: "Base units" },
    { key: "additional_units", label: "Additional units" },
    { key: "conversion", label: "Conversion", type: "number" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 50 },
    { name: "formal_name", label: "Formal name", type: "text", maxLength: 100 },
    { name: "is_simple_unit", label: "Is simple unit", type: "checkbox", default: true },
    { name: "base_units", label: "Base units", type: "text", maxLength: 100 },
    { name: "additional_units", label: "Additional units", type: "text", maxLength: 100 },
    { name: "conversion", label: "Conversion", type: "number", step: 0.01, default: 1 },
  ],
};

export const godowns = {
  key: "godowns",
  title: "Godowns",
  singular: "Godown",
  endpoint: "/inventory/godowns/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "city", label: "City" },
    { key: "incharge", label: "Incharge" },
    { key: "mobile", label: "Mobile" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
    { name: "parent", label: "Parent", type: "text", maxLength: 200 },
    { name: "address", label: "Address", type: "textarea" },
    { name: "city", label: "City", type: "text", maxLength: 100 },
    { name: "state", label: "State", type: "text", maxLength: 100 },
    { name: "pincode", label: "Pincode", type: "text", maxLength: 10 },
    { name: "incharge", label: "Incharge", type: "text", maxLength: 100 },
    { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const batches = {
  key: "batches",
  title: "Batches",
  singular: "Batch",
  endpoint: "/inventory/batches/",
  search: true,
  columns: [
    { key: "item_name", label: "Item" },
    { key: "batch_no", label: "Batch No" },
    { key: "mfg_date", label: "Mfg date", type: "date" },
    { key: "exp_date", label: "Exp date", type: "date" },
    { key: "quantity", label: "Quantity", type: "number" },
    { key: "godown", label: "Godown" },
  ],
  fields: [
    { name: "item", label: "Item", type: "relation", lookup: "items", required: true },
    { name: "item_name", label: "Item name", type: "text", required: true, maxLength: 200 },
    { name: "batch_no", label: "Batch No", type: "text", required: true, maxLength: 100 },
    { name: "mfg_date", label: "Mfg date", type: "date" },
    { name: "exp_date", label: "Exp date", type: "date" },
    { name: "quantity", label: "Quantity", type: "number", step: 0.01 },
    { name: "godown", label: "Godown", type: "text", maxLength: 100 },
  ],
};

export const journals = {
  key: "journals",
  title: "Stock Journal",
  singular: "Stock Journal Entry",
  endpoint: "/inventory/journals/",
  search: true,
  columns: [
    { key: "date", label: "Date", type: "date" },
    { key: "item_name", label: "Item" },
    { key: "type", label: "Type", type: "badge" },
    { key: "quantity", label: "Quantity", type: "number" },
    { key: "rate", label: "Rate", type: "number" },
    { key: "godown", label: "Godown" },
  ],
  fields: [
    { name: "date", label: "Date", type: "date", required: true },
    { name: "item", label: "Item", type: "relation", lookup: "items", required: true },
    { name: "item_name", label: "Item name", type: "text", required: true, maxLength: 200 },
    { name: "type", label: "Type", type: "select", options: ["IN", "OUT", "TRANSFER"], required: true },
    { name: "quantity", label: "Quantity", type: "number", step: 0.01, required: true },
    { name: "rate", label: "Rate", type: "number", step: 0.01 },
    { name: "godown", label: "Godown", type: "text", maxLength: 100 },
    { name: "destination_godown", label: "Destination godown", type: "text", maxLength: 100 },
    { name: "reference", label: "Reference", type: "text", maxLength: 200 },
  ],
  filters: ["type"],
};

export const mrn = {
  key: "mrn",
  title: "Material Receipts (MRN)",
  singular: "Material Receipt",
  endpoint: "/inventory/mrn/",
  search: true,
  columns: [
    { key: "mrn_no", label: "MRN No" },
    { key: "date", label: "Date", type: "date" },
    { key: "supplier_name", label: "Supplier name" },
    { key: "status", label: "Status" },
  ],
  fields: [
    { name: "mrn_no", label: "MRN No", type: "text", required: true, maxLength: 100 },
    { name: "date", label: "Date", type: "date", required: true },
    { name: "supplier_name", label: "Supplier name", type: "text", required: true, maxLength: 200 },
    { name: "supplier_invoice", label: "Supplier invoice", type: "text", maxLength: 100 },
    { name: "transporter", label: "Transporter", type: "text", maxLength: 100 },
    { name: "vehicle_no", label: "Vehicle No", type: "text", maxLength: 20 },
    { name: "godown", label: "Godown", type: "text", maxLength: 100 },
    { name: "eway_bill", label: "Eway bill", type: "text", maxLength: 50 },
    { name: "remarks", label: "Remarks", type: "textarea" },
    { name: "status", label: "Status", type: "text", default: "completed", maxLength: 20 },
  ],
};

export const resources = [stockItems, groups, categories, units, godowns, batches, journals, mrn];
