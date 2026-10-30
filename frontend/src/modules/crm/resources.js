// ----------------------------------------------------------------------------
// CRM module - screens that are plain "list + add/edit form" tables.
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

export const customers = {
  key: "customers",
  title: "Customers",
  singular: "Customer",
  endpoint: "/crm/customers/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "customer_type", label: "Customer type", type: "badge" },
    { key: "contact_person", label: "Contact person" },
    { key: "mobile", label: "Mobile" },
    { key: "city", label: "City" },
    { key: "status", label: "Status", type: "badge" },
  ],
  sections: [
    { title: "Basic", fields: [
      { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
      { name: "company", label: "Company", type: "text", maxLength: 200 },
      { name: "customer_type", label: "Customer type", type: "select", options: ["customer", "supplier", "both"], default: "customer" },
      { name: "status", label: "Status", type: "select", options: ["active", "inactive", "blocked"], default: "active" },
      { name: "contact_person", label: "Contact person", type: "text", maxLength: 100 },
      { name: "designation", label: "Designation", type: "text", maxLength: 100 },
      { name: "department", label: "Department", type: "text", maxLength: 100 },
      { name: "source", label: "Source", type: "text", maxLength: 100 },
      { name: "industry", label: "Industry", type: "text", maxLength: 100 },
    ] },
    { title: "Contact", fields: [
      { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
      { name: "alt_mobile", label: "Alt mobile", type: "text", maxLength: 15 },
      { name: "email", label: "Email", type: "email" },
      { name: "website", label: "Website", type: "url" },
      { name: "address_billing", label: "Address billing", type: "textarea" },
      { name: "address_shipping", label: "Address shipping", type: "textarea" },
      { name: "city", label: "City", type: "text", maxLength: 100 },
      { name: "state", label: "State", type: "text", maxLength: 100 },
      { name: "pincode", label: "Pincode", type: "text", maxLength: 10 },
      { name: "country", label: "Country", type: "text", default: "India", maxLength: 50 },
    ] },
    { title: "Tax & credit", fields: [
      { name: "gstin", label: "GSTIN", type: "text", maxLength: 15 },
      { name: "pan", label: "PAN", type: "text", maxLength: 10 },
      { name: "msme_no", label: "MSME No", type: "text", maxLength: 50 },
      { name: "tax_registration_type", label: "Tax registration type", type: "text", maxLength: 50 },
      { name: "credit_limit", label: "Credit limit", type: "number", step: 0.01 },
      { name: "credit_period", label: "Credit period", type: "number", step: 1, default: 30 },
      { name: "payment_terms", label: "Payment terms", type: "text", maxLength: 100 },
      { name: "price_category", label: "Price category", type: "text", maxLength: 50 },
    ] },
    { title: "Bank", fields: [
      { name: "bank_name", label: "Bank name", type: "text", maxLength: 100 },
      { name: "bank_account", label: "Bank account", type: "text", maxLength: 50 },
      { name: "bank_ifsc", label: "Bank IFSC", type: "text", maxLength: 20 },
      { name: "notes", label: "Notes", type: "textarea" },
    ] },
  ],
  filters: ["customer_type", "status"],
};

export const leads = {
  key: "leads",
  title: "Leads",
  singular: "Lead",
  endpoint: "/crm/leads/",
  search: true,
  columns: [
    { key: "company", label: "Company" },
    { key: "contact_person", label: "Contact person" },
    { key: "mobile", label: "Mobile" },
    { key: "source", label: "Source" },
    { key: "priority", label: "Priority", type: "badge" },
    { key: "status", label: "Status", type: "badge" },
    { key: "follow_up_date", label: "Follow up date", type: "date" },
  ],
  fields: [
    { name: "company", label: "Company", type: "text", required: true, maxLength: 200 },
    { name: "contact_person", label: "Contact person", type: "text", maxLength: 100 },
    { name: "email", label: "Email", type: "email" },
    { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
    { name: "source", label: "Source", type: "text", maxLength: 100 },
    { name: "industry", label: "Industry", type: "text", maxLength: 100 },
    { name: "status", label: "Status", type: "select", options: ["new", "contacted", "qualified", "converted", "lost"], default: "new" },
    { name: "priority", label: "Priority", type: "select", options: ["high", "medium", "low"], default: "medium" },
    { name: "assigned_to", label: "Assigned to", type: "text", maxLength: 100 },
    { name: "notes", label: "Notes", type: "textarea" },
    { name: "follow_up_date", label: "Follow up date", type: "date" },
  ],
  filters: ["status", "priority"],
};

export const inquiries = {
  key: "inquiries",
  title: "Purchase Inquiries",
  singular: "Inquiry",
  endpoint: "/crm/inquiries/",
  search: true,
  columns: [
    { key: "inquiry_no", label: "Inquiry No" },
    { key: "date", label: "Date", type: "date" },
    { key: "supplier_name", label: "Supplier name" },
    { key: "item_required", label: "Item required" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "inquiry_no", label: "Inquiry No", type: "text", required: true, maxLength: 100 },
    { name: "date", label: "Date", type: "date", required: true },
    { name: "supplier_name", label: "Supplier name", type: "text", required: true, maxLength: 200 },
    { name: "contact_person", label: "Contact person", type: "text", maxLength: 100 },
    { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
    { name: "email", label: "Email", type: "email" },
    { name: "gstin", label: "GSTIN", type: "text", maxLength: 15 },
    { name: "item_required", label: "Item required", type: "text", required: true, maxLength: 200 },
    { name: "quantity", label: "Quantity", type: "number", step: 0.01 },
    { name: "uom", label: "UOM", type: "text", maxLength: 50 },
    { name: "expected_rate", label: "Expected rate", type: "number", step: 0.01 },
    { name: "expected_date", label: "Expected date", type: "date" },
    { name: "payment_terms", label: "Payment terms", type: "text", maxLength: 100 },
    { name: "status", label: "Status", type: "select", options: ["open", "approved", "rejected", "closed", "converted"], default: "open" },
    { name: "priority", label: "Priority", type: "text", default: "medium", maxLength: 10 },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["status"],
};

export const quotations = {
  key: "quotations",
  title: "Quotations",
  singular: "Quotation",
  endpoint: "/crm/quotations/",
  search: true,
  columns: [
    { key: "quote_no", label: "Quote No" },
    { key: "date", label: "Date", type: "date" },
    { key: "customer_name", label: "Customer name" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "quote_no", label: "Quote No", type: "text", required: true, maxLength: 100 },
    { name: "date", label: "Date", type: "date", required: true },
    { name: "valid_upto", label: "Valid upto", type: "date" },
    { name: "customer_name", label: "Customer name", type: "text", required: true, maxLength: 200 },
    { name: "customer_contact", label: "Customer contact", type: "text", maxLength: 100 },
    { name: "customer_mobile", label: "Customer mobile", type: "text", maxLength: 15 },
    { name: "customer_email", label: "Customer email", type: "email" },
    { name: "customer_gstin", label: "Customer GSTIN", type: "text", maxLength: 15 },
    { name: "billing_address", label: "Billing address", type: "text" },
    { name: "shipping_address", label: "Shipping address", type: "text" },
    { name: "reference", label: "Reference", type: "text", maxLength: 200 },
    { name: "payment_terms", label: "Payment terms", type: "text", maxLength: 200 },
    { name: "delivery_terms", label: "Delivery terms", type: "text", maxLength: 200 },
    { name: "delivery_time", label: "Delivery time", type: "text", maxLength: 100 },
    { name: "freight", label: "Freight", type: "text", maxLength: 100 },
    { name: "warranty", label: "Warranty", type: "text", maxLength: 100 },
    { name: "subtotal", label: "Subtotal", type: "number", step: 0.01 },
    { name: "cgst", label: "Cgst", type: "number", step: 0.01 },
    { name: "sgst", label: "Sgst", type: "number", step: 0.01 },
    { name: "igst", label: "Igst", type: "number", step: 0.01 },
    { name: "total", label: "Total", type: "number", step: 0.01 },
    { name: "status", label: "Status", type: "select", options: ["pending", "approved", "rejected", "converted"], default: "pending" },
    { name: "prepared_by", label: "Prepared by", type: "text", maxLength: 100 },
    { name: "remarks", label: "Remarks", type: "textarea" },
    { name: "terms_conditions", label: "Terms conditions", type: "text" },
  ],
  filters: ["status"],
};

export const purchaseOrders = {
  key: "purchase-orders",
  title: "Purchase Orders",
  singular: "Purchase Order",
  endpoint: "/crm/purchase-orders/",
  search: true,
  columns: [
    { key: "po_no", label: "PO No" },
    { key: "date", label: "Date", type: "date" },
    { key: "supplier_name", label: "Supplier name" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "po_no", label: "PO No", type: "text", required: true, maxLength: 100 },
    { name: "date", label: "Date", type: "date", required: true },
    { name: "delivery_date", label: "Delivery date", type: "date" },
    { name: "reference", label: "Reference", type: "text", maxLength: 200 },
    { name: "supplier_name", label: "Supplier name", type: "text", required: true, maxLength: 200 },
    { name: "contact_person", label: "Contact person", type: "text", maxLength: 100 },
    { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
    { name: "email", label: "Email", type: "email" },
    { name: "gstin", label: "GSTIN", type: "text", maxLength: 15 },
    { name: "supplier_address", label: "Supplier address", type: "text" },
    { name: "payment_terms", label: "Payment terms", type: "text", maxLength: 200 },
    { name: "delivery_terms", label: "Delivery terms", type: "text", maxLength: 200 },
    { name: "freight", label: "Freight", type: "text", maxLength: 100 },
    { name: "subtotal", label: "Subtotal", type: "number", step: 0.01 },
    { name: "cgst", label: "Cgst", type: "number", step: 0.01 },
    { name: "sgst", label: "Sgst", type: "number", step: 0.01 },
    { name: "total", label: "Total", type: "number", step: 0.01 },
    { name: "status", label: "Status", type: "select", options: ["open", "received", "cancelled"], default: "open" },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["status"],
};

export const resources = [customers, leads, inquiries, quotations, purchaseOrders];
