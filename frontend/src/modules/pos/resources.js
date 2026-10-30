// ----------------------------------------------------------------------------
// POS module - screens that are plain "list + add/edit form" tables.
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

export const sales = {
  key: "sales",
  title: "Sales",
  singular: "Sale",
  endpoint: "/pos/sales/",
  search: true,
  columns: [
    { key: "invoice_no", label: "Invoice No" },
    { key: "counter_name", label: "Counter" },
    { key: "invoice_date", label: "Invoice date", type: "date" },
    { key: "payment_method", label: "Payment method" },
  ],
  fields: [
    { name: "invoice_no", label: "Invoice No", type: "text", required: true, maxLength: 100 },
    { name: "counter", label: "Counter", type: "relation", lookup: "counters" },
    { name: "session", label: "Session", type: "relation", lookup: "posSessions" },
    { name: "invoice_date", label: "Invoice date", type: "date", required: true },
    { name: "payment_method", label: "Payment method", type: "text", maxLength: 100 },
  ],
};

export const counters = {
  key: "counters",
  title: "Counters",
  singular: "Counter",
  endpoint: "/pos/counters/",
  search: true,
  columns: [
    { key: "counter_name", label: "Counter name" },
    { key: "counter_code", label: "Counter code" },
    { key: "location", label: "Location" },
    { key: "printer_name", label: "Printer name" },
    { key: "receipt_header", label: "Receipt header" },
    { key: "receipt_footer", label: "Receipt footer" },
  ],
  fields: [
    { name: "counter_name", label: "Counter name", type: "text", required: true, maxLength: 100 },
    { name: "counter_code", label: "Counter code", type: "text", required: true, maxLength: 20 },
    { name: "branch", label: "Branch", type: "relation", lookup: "branches" },
    { name: "godown", label: "Godown", type: "relation", lookup: "godowns" },
    { name: "location", label: "Location", type: "text", maxLength: 200 },
    { name: "printer_name", label: "Printer name", type: "text", maxLength: 100 },
    { name: "receipt_header", label: "Receipt header", type: "text" },
    { name: "receipt_footer", label: "Receipt footer", type: "text" },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const sessions = {
  key: "sessions",
  title: "Sessions",
  singular: "Session",
  endpoint: "/pos/sessions/",
  search: true,
  columns: [
    { key: "counter_name", label: "Counter" },
    { key: "session_date", label: "Session date", type: "date" },
    { key: "opening_time", label: "Opening time", type: "datetime" },
    { key: "closing_time", label: "Closing time", type: "datetime" },
    { key: "opening_balance", label: "Opening balance", type: "money" },
    { key: "closing_balance", label: "Closing balance", type: "money" },
  ],
  fields: [
    { name: "counter", label: "Counter", type: "relation", lookup: "counters", required: true },
    { name: "session_date", label: "Session date", type: "date", required: true },
    { name: "opening_time", label: "Opening time", type: "datetime" },
    { name: "closing_time", label: "Closing time", type: "datetime" },
    { name: "opening_balance", label: "Opening balance", type: "number", step: 0.01 },
    { name: "closing_balance", label: "Closing balance", type: "number", step: 0.01 },
    { name: "expected_cash", label: "Expected cash", type: "number", step: 0.01 },
    { name: "actual_cash", label: "Actual cash", type: "number", step: 0.01 },
    { name: "opened_by", label: "Opened by", type: "relation", lookup: "users" },
    { name: "closed_by", label: "Closed by", type: "relation", lookup: "users" },
    { name: "status", label: "Status", type: "select", options: ["open", "closed", "reconciled"], default: "open" },
    { name: "notes", label: "Notes", type: "textarea" },
  ],
  filters: ["status"],
};

export const priceLists = {
  key: "price-lists",
  title: "Price Lists",
  singular: "Price List",
  endpoint: "/pos/price-lists/",
  search: true,
  columns: [
    { key: "price_list_name", label: "Price list name" },
    { key: "price_list_code", label: "Price list code" },
    { key: "is_inclusive_tax", label: "Is inclusive tax", type: "bool" },
    { key: "is_active", label: "Is active", type: "bool" },
    { key: "is_default", label: "Is default", type: "bool" },
  ],
  fields: [
    { name: "price_list_name", label: "Price list name", type: "text", required: true, maxLength: 100 },
    { name: "price_list_code", label: "Price list code", type: "text", required: true, maxLength: 50 },
    { name: "is_inclusive_tax", label: "Is inclusive tax", type: "checkbox", default: true },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
    { name: "is_default", label: "Is default", type: "checkbox" },
  ],
};

export const prices = {
  key: "prices",
  title: "Item Prices",
  singular: "Item Price",
  endpoint: "/pos/prices/",
  search: true,
  columns: [
    { key: "item_name", label: "Item" },
    { key: "price_list_name", label: "Price list" },
    { key: "mrp", label: "Mrp", type: "number" },
    { key: "selling_price", label: "Selling price", type: "money" },
    { key: "wholesale_price", label: "Wholesale price", type: "money" },
    { key: "discount_allowed", label: "Discount allowed", type: "bool" },
  ],
  fields: [
    { name: "item", label: "Item", type: "relation", lookup: "items", required: true },
    { name: "price_list", label: "Price list", type: "relation", lookup: "priceLists", required: true },
    { name: "mrp", label: "Mrp", type: "number", step: 0.01 },
    { name: "selling_price", label: "Selling price", type: "number", step: 0.01, required: true },
    { name: "wholesale_price", label: "Wholesale price", type: "number", step: 0.01 },
    { name: "discount_allowed", label: "Discount allowed", type: "checkbox", default: true },
    { name: "max_discount_percent", label: "Max discount percent", type: "number", step: 0.01, default: 100 },
  ],
};

export const paymentMethods = {
  key: "payment-methods",
  title: "Payment Methods",
  singular: "Payment Method",
  endpoint: "/pos/payment-methods/",
  search: true,
  columns: [
    { key: "method_name", label: "Method name" },
    { key: "method_code", label: "Method code" },
    { key: "method_type", label: "Method type", type: "badge" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "method_name", label: "Method name", type: "text", required: true, maxLength: 100 },
    { name: "method_code", label: "Method code", type: "text", required: true, maxLength: 50 },
    { name: "method_type", label: "Method type", type: "select", options: ["cash", "card", "upi", "wallet", "bank_transfer"], required: true },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
  filters: ["method_type"],
};

export const payments = {
  key: "payments",
  title: "Payments",
  singular: "Payment",
  endpoint: "/pos/payments/",
  search: true,
  columns: [
    { key: "amount", label: "Amount", type: "money" },
    { key: "reference_number", label: "Reference number" },
    { key: "transaction_id", label: "Transaction ID" },
    { key: "status", label: "Status" },
  ],
  fields: [
    { name: "sale", label: "Sale", type: "relation", lookup: "posSales", required: true },
    { name: "payment_method", label: "Payment method", type: "relation", lookup: "paymentMethods", required: true },
    { name: "amount", label: "Amount", type: "number", step: 0.01, required: true },
    { name: "reference_number", label: "Reference number", type: "text", maxLength: 100 },
    { name: "transaction_id", label: "Transaction ID", type: "text", maxLength: 200 },
    { name: "status", label: "Status", type: "text", default: "completed", maxLength: 20 },
  ],
};

export const resources = [sales, counters, sessions, priceLists, prices, paymentMethods, payments];
