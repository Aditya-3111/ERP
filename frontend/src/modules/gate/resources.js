// ----------------------------------------------------------------------------
// Gate module - screens that are plain "list + add/edit form" tables.
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

export const visitors = {
  key: "visitors",
  title: "Visitors",
  singular: "Visitor",
  endpoint: "/gate/visitors/",
  search: true,
  columns: [
    { key: "visitor_id", label: "Visitor ID" },
    { key: "name", label: "Name" },
    { key: "company", label: "Company" },
    { key: "purpose", label: "Purpose" },
    { key: "host_employee", label: "Host employee" },
    { key: "entry_date", label: "Entry date", type: "date" },
    { key: "status", label: "Status", type: "badge" },
  ],
  sections: [
    { title: "Visitor", fields: [
      { name: "visitor_id", label: "Visitor ID", type: "text", required: true, maxLength: 50 },
      { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
      { name: "company", label: "Company", type: "text", maxLength: 200 },
      { name: "designation", label: "Designation", type: "text", maxLength: 100 },
      { name: "mobile", label: "Mobile", type: "text", required: true, maxLength: 15 },
      { name: "email", label: "Email", type: "email" },
      { name: "gender", label: "Gender", type: "select", options: ["Male", "Female", "Other"] },
      { name: "visitor_category", label: "Visitor category", type: "text", default: "General", maxLength: 50 },
      { name: "no_of_persons", label: "No of persons", type: "number", step: 1, default: 1 },
    ] },
    { title: "Visit", fields: [
      { name: "purpose", label: "Purpose", type: "text", required: true, maxLength: 100 },
      { name: "host_employee", label: "Host employee", type: "text", required: true, maxLength: 200 },
      { name: "host_department", label: "Host department", type: "text", maxLength: 100 },
      { name: "entry_date", label: "Entry date", type: "date", required: true },
      { name: "entry_time", label: "Entry time", type: "time", required: true },
      { name: "exit_time", label: "Exit time", type: "time" },
      { name: "expected_duration", label: "Expected duration", type: "number", step: 1, default: 60 },
      { name: "status", label: "Status", type: "select", options: ["checked_in", "checked_out"], default: "checked_in" },
      { name: "badge_no", label: "Badge No", type: "text", maxLength: 50 },
      { name: "security_by", label: "Security by", type: "text", maxLength: 100 },
    ] },
    { title: "ID & vehicle", fields: [
      { name: "id_proof_type", label: "ID proof type", type: "text", maxLength: 50 },
      { name: "id_proof_number", label: "ID proof number", type: "text", maxLength: 50 },
      { name: "vehicle_no", label: "Vehicle No", type: "text", maxLength: 20 },
      { name: "vehicle_type", label: "Vehicle type", type: "text", maxLength: 50 },
      { name: "belongings", label: "Belongings", type: "text", maxLength: 255 },
      { name: "nda_signed", label: "NDA signed", type: "checkbox" },
      { name: "safety_briefing", label: "Safety briefing", type: "checkbox" },
      { name: "remarks", label: "Remarks", type: "textarea" },
    ] },
  ],
  filters: ["status"],
};

export const entries = {
  key: "entries",
  title: "Gate Entries",
  singular: "Gate Entry",
  endpoint: "/gate/entries/",
  search: true,
  columns: [
    { key: "date", label: "Date", type: "date" },
    { key: "type", label: "Type", type: "badge" },
    { key: "status", label: "Status", type: "badge" },
  ],
  fields: [
    { name: "gate_pass_no", label: "Gate pass No", type: "text", maxLength: 100 },
    { name: "date", label: "Date", type: "date", required: true },
    { name: "time", label: "Time", type: "time" },
    { name: "type", label: "Type", type: "select", options: ["INWARD", "OUTWARD"], required: true },
    { name: "vehicle_no", label: "Vehicle No", type: "text", maxLength: 20 },
    { name: "vehicle_type", label: "Vehicle type", type: "text", maxLength: 50 },
    { name: "transporter", label: "Transporter", type: "text", maxLength: 200 },
    { name: "party_name", label: "Party name", type: "text", maxLength: 200 },
    { name: "material", label: "Material", type: "text", maxLength: 200 },
    { name: "quantity", label: "Quantity", type: "number", step: 0.01 },
    { name: "uom", label: "UOM", type: "text", maxLength: 50 },
    { name: "challan_no", label: "Challan No", type: "text", maxLength: 100 },
    { name: "driver_name", label: "Driver name", type: "text", maxLength: 100 },
    { name: "driver_mobile", label: "Driver mobile", type: "text", maxLength: 15 },
    { name: "security_check", label: "Security check", type: "text", maxLength: 100 },
    { name: "exit_time", label: "Exit time", type: "time" },
    { name: "status", label: "Status", type: "select", options: ["PENDING", "AT_GATE", "COMPLETED"], default: "AT_GATE" },
    { name: "remarks", label: "Remarks", type: "textarea" },
  ],
  filters: ["type", "status"],
};

export const transporters = {
  key: "transporters",
  title: "Transporters",
  singular: "Transporter",
  endpoint: "/gate/transporters/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "contact", label: "Contact" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
    { name: "contact", label: "Contact", type: "text", maxLength: 50 },
    { name: "address", label: "Address", type: "textarea" },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const logs = {
  key: "logs",
  title: "Visitor Logs",
  singular: "Log",
  endpoint: "/gate/logs/",
  search: true,
  columns: [
    { key: "visitor_name", label: "Visitor" },
    { key: "action", label: "Action", type: "badge" },
  ],
  fields: [
    { name: "visitor", label: "Visitor", type: "relation", lookup: "visitors", required: true },
    { name: "action", label: "Action", type: "select", options: ["CHECK_IN", "CHECK_OUT"], required: true },
    { name: "details", label: "Details", type: "textarea" },
  ],
  filters: ["action"],
};

export const resources = [visitors, entries, transporters, logs];
