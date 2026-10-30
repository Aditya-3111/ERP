// ----------------------------------------------------------------------------
// Finance module - screens that are plain "list + add/edit form" tables.
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

export const ledgers = {
  key: "ledgers",
  title: "Ledgers",
  singular: "Ledger",
  endpoint: "/finance/ledgers/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
    { key: "opening_balance", label: "Opening balance", type: "money" },
    { key: "opening_balance_type", label: "Opening balance type", type: "badge" },
    { key: "gstin", label: "GSTIN" },
    { key: "city", label: "City" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  sections: [
    { title: "Basic", fields: [
      { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
      { name: "parent", label: "Parent", type: "text", maxLength: 200 },
      { name: "alias", label: "Alias", type: "text", maxLength: 100 },
      { name: "opening_balance", label: "Opening balance", type: "number", step: 0.01 },
      { name: "opening_balance_type", label: "Opening balance type", type: "select", options: ["dr", "cr"], default: "dr" },
      { name: "is_active", label: "Is active", type: "checkbox", default: true },
      { name: "description", label: "Description", type: "textarea" },
      { name: "notes", label: "Notes", type: "textarea" },
    ] },
    { title: "Contact", fields: [
      { name: "mailing_name", label: "Mailing name", type: "text", maxLength: 200 },
      { name: "contact_person", label: "Contact person", type: "text", maxLength: 100 },
      { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
      { name: "phone", label: "Phone", type: "text", maxLength: 15 },
      { name: "email", label: "Email", type: "email" },
      { name: "website", label: "Website", type: "url" },
      { name: "address", label: "Address", type: "textarea" },
      { name: "city", label: "City", type: "text", maxLength: 100 },
      { name: "state", label: "State", type: "text", maxLength: 100 },
      { name: "country", label: "Country", type: "text", maxLength: 100 },
      { name: "pincode", label: "Pincode", type: "text", maxLength: 10 },
    ] },
    { title: "Tax", fields: [
      { name: "gstin", label: "GSTIN", type: "text", maxLength: 15 },
      { name: "pan", label: "PAN", type: "text", maxLength: 10 },
      { name: "gst_registration_type", label: "GST registration type", type: "text", maxLength: 50 },
      { name: "gst_supply_type", label: "GST supply type", type: "text", maxLength: 50 },
      { name: "gst_duty_head", label: "GST duty head", type: "text", maxLength: 20 },
      { name: "msme_no", label: "MSME No", type: "text", maxLength: 50 },
    ] },
    { title: "Bank & credit", fields: [
      { name: "bank_account_holder", label: "Bank account holder", type: "text", maxLength: 200 },
      { name: "bank_account_number", label: "Bank account number", type: "text", maxLength: 50 },
      { name: "bank_ifsc", label: "Bank IFSC", type: "text", maxLength: 20 },
      { name: "bank_swift", label: "Bank swift", type: "text", maxLength: 20 },
      { name: "bank_name", label: "Bank name", type: "text", maxLength: 100 },
      { name: "bank_branch", label: "Bank branch", type: "text", maxLength: 200 },
      { name: "bill_credit_period", label: "Bill credit period", type: "number", step: 1 },
      { name: "credit_limit", label: "Credit limit", type: "number", step: 0.01 },
    ] },
    { title: "Other", fields: [
      { name: "is_revenue", label: "Is revenue", type: "checkbox" },
      { name: "is_deemed_positive", label: "Is deemed positive", type: "checkbox" },
    ] },
  ],
  filters: ["opening_balance_type"],
};

export const accountGroups = {
  key: "account-groups",
  title: "Account Groups",
  singular: "Account Group",
  endpoint: "/finance/account-groups/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
    { key: "primary_group", label: "Primary group" },
    { key: "is_revenue", label: "Is revenue", type: "bool" },
    { key: "is_deemed_positive", label: "Is deemed positive", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
    { name: "parent", label: "Parent", type: "text", maxLength: 200 },
    { name: "primary_group", label: "Primary group", type: "text", maxLength: 200 },
    { name: "is_revenue", label: "Is revenue", type: "checkbox" },
    { name: "is_deemed_positive", label: "Is deemed positive", type: "checkbox" },
    { name: "affects_gross_profit", label: "Affects gross profit", type: "checkbox" },
    { name: "sort_position", label: "Sort position", type: "number", step: 1 },
  ],
};

export const voucherTypes = {
  key: "voucher-types",
  title: "Voucher Types",
  singular: "Voucher Type",
  endpoint: "/finance/voucher-types/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
    { key: "numbering_method", label: "Numbering method" },
    { key: "affects_stock", label: "Affects stock", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 100 },
    { name: "parent", label: "Parent", type: "text", maxLength: 100 },
    { name: "numbering_method", label: "Numbering method", type: "text", maxLength: 50 },
    { name: "is_deemed_positive", label: "Is deemed positive", type: "checkbox" },
    { name: "affects_stock", label: "Affects stock", type: "checkbox" },
  ],
};

export const resources = [ledgers, accountGroups, voucherTypes];
