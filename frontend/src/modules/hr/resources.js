// ----------------------------------------------------------------------------
// HR module - screens that are plain "list + add/edit form" tables.
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

export const employees = {
  key: "employees",
  title: "Employees",
  singular: "Employee",
  endpoint: "/hr/employees/",
  search: true,
  columns: [
    { key: "emp_code", label: "Emp code" },
    { key: "name", label: "Name" },
    { key: "department", label: "Department" },
    { key: "designation", label: "Designation" },
    { key: "mobile", label: "Mobile" },
    { key: "salary", label: "Salary", type: "money" },
    { key: "status", label: "Status", type: "badge" },
  ],
  sections: [
    { title: "Job", fields: [
      { name: "emp_code", label: "Emp code", type: "text", required: true, maxLength: 50 },
      { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
      { name: "department", label: "Department", type: "text", maxLength: 100 },
      { name: "designation", label: "Designation", type: "text", maxLength: 100 },
      { name: "function_role", label: "Function role", type: "text", maxLength: 100 },
      { name: "location", label: "Location", type: "text", maxLength: 200 },
      { name: "date_of_joining", label: "Date of joining", type: "date" },
      { name: "date_of_release", label: "Date of release", type: "date" },
      { name: "salary", label: "Salary", type: "number", step: 0.01 },
      { name: "status", label: "Status", type: "select", options: ["active", "inactive", "resigned", "terminated"], default: "active" },
    ] },
    { title: "Personal", fields: [
      { name: "gender", label: "Gender", type: "select", options: ["Male", "Female", "Other"] },
      { name: "date_of_birth", label: "Date of birth", type: "date" },
      { name: "blood_group", label: "Blood group", type: "text", maxLength: 10 },
      { name: "father_mother_name", label: "Father mother name", type: "text", maxLength: 200 },
      { name: "spouse_name", label: "Spouse name", type: "text", maxLength: 200 },
      { name: "mobile", label: "Mobile", type: "text", maxLength: 15 },
      { name: "email", label: "Email", type: "email" },
      { name: "address", label: "Address", type: "textarea" },
      { name: "city", label: "City", type: "text", maxLength: 100 },
      { name: "state", label: "State", type: "text", maxLength: 100 },
      { name: "pincode", label: "Pincode", type: "text", maxLength: 10 },
    ] },
    { title: "IDs", fields: [
      { name: "pan", label: "PAN", type: "text", maxLength: 10 },
      { name: "aadhaar", label: "Aadhaar", type: "text", maxLength: 12 },
      { name: "uan", label: "UAN", type: "text", maxLength: 20 },
      { name: "pf_number", label: "PF number", type: "text", maxLength: 50 },
      { name: "remarks", label: "Remarks", type: "textarea" },
    ] },
  ],
  filters: ["status", "gender"],
};

export const departments = {
  key: "departments",
  title: "Departments",
  singular: "Department",
  endpoint: "/hr/departments/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "description", label: "Description" },
    { key: "is_active", label: "Is active", type: "bool" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 100 },
    { name: "description", label: "Description", type: "textarea" },
    { name: "is_active", label: "Is active", type: "checkbox", default: true },
  ],
};

export const designations = {
  key: "designations",
  title: "Designations",
  singular: "Designation",
  endpoint: "/hr/designations/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "department_name", label: "Department" },
    { key: "description", label: "Description" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 100 },
    { name: "department", label: "Department", type: "relation", lookup: "departments" },
    { name: "description", label: "Description", type: "textarea" },
  ],
};

export const attendance = {
  key: "attendance",
  title: "Attendance Records",
  singular: "Attendance",
  endpoint: "/hr/attendance/",
  search: true,
  columns: [
    { key: "date", label: "Date", type: "date" },
    { key: "employee_name", label: "Employee" },
    { key: "status", label: "Status", type: "badge" },
    { key: "in_time", label: "In time" },
    { key: "out_time", label: "Out time" },
  ],
  fields: [
    { name: "employee", label: "Employee", type: "relation", lookup: "employees", required: true },
    { name: "date", label: "Date", type: "date", required: true },
    { name: "in_time", label: "In time", type: "time" },
    { name: "out_time", label: "Out time", type: "time" },
    { name: "status", label: "Status", type: "select", options: ["Present", "Absent", "Half Day", "Leave", "Holiday"], default: "Present" },
    { name: "remarks", label: "Remarks", type: "textarea", maxLength: 255 },
  ],
  filters: ["status"],
};

export const payheads = {
  key: "payheads",
  title: "Pay Heads",
  singular: "Pay Head",
  endpoint: "/hr/payheads/",
  search: true,
  columns: [
    { key: "name", label: "Name" },
    { key: "parent", label: "Parent" },
    { key: "payslip_name", label: "Payslip name" },
    { key: "pay_type", label: "Pay type", type: "badge" },
    { key: "income_type", label: "Income type" },
    { key: "calculation_type", label: "Calculation type" },
  ],
  fields: [
    { name: "name", label: "Name", type: "text", required: true, maxLength: 200 },
    { name: "parent", label: "Parent", type: "text", maxLength: 200 },
    { name: "payslip_name", label: "Payslip name", type: "text", maxLength: 200 },
    { name: "pay_type", label: "Pay type", type: "select", options: ["Earning", "Deduction"], required: true },
    { name: "income_type", label: "Income type", type: "text", maxLength: 50 },
    { name: "calculation_type", label: "Calculation type", type: "text", maxLength: 50 },
    { name: "leave_type", label: "Leave type", type: "text", maxLength: 50 },
    { name: "calculation_period", label: "Calculation period", type: "text", maxLength: 50 },
  ],
  filters: ["pay_type"],
};

export const documents = {
  key: "documents",
  title: "Employee Documents",
  singular: "Document",
  endpoint: "/hr/documents/",
  search: true,
  columns: [
    { key: "employee_name", label: "Employee" },
    { key: "document_type", label: "Document type" },
    { key: "document_name", label: "Document name" },
  ],
  fields: [
    { name: "employee", label: "Employee", type: "relation", lookup: "employees", required: true },
    { name: "document_type", label: "Document type", type: "text", required: true, maxLength: 100 },
    { name: "document_name", label: "Document name", type: "text", required: true, maxLength: 200 },
    { name: "document_file", label: "Document file", type: "file", required: true },
  ],
};

export const resources = [employees, departments, designations, attendance, payheads, documents];
