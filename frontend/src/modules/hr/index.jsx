// HR module: employees, departments ... + attendance marking and payroll pages.
import { resources } from './resources.js';
import AttendancePage from './pages/AttendancePage.jsx';
import PayrollPage from './pages/PayrollPage.jsx';

// "Attendance Records" is the plain table; "Mark Attendance" is the daily bulk page.
const records = { ...resources.find((r) => r.key === 'attendance'), key: 'attendance-records', title: 'Attendance Records' };

export default {
  key: 'hr',
  title: 'HR',
  icon: 'hr',
  resources: [...resources.filter((r) => r.key !== 'attendance'), records],
  routes: [
    { path: 'attendance', element: <AttendancePage /> },
    { path: 'payroll', element: <PayrollPage /> },
  ],
  menu: [
    { label: 'Employees', path: '/hr/employees' },
    { label: 'Mark Attendance', path: '/hr/attendance' },
    { label: 'Attendance Records', path: '/hr/attendance-records' },
    { label: 'Payroll', path: '/hr/payroll' },
    { label: 'Departments', path: '/hr/departments' },
    { label: 'Designations', path: '/hr/designations' },
    { label: 'Pay Heads', path: '/hr/payheads' },
    { label: 'Documents', path: '/hr/documents' },
  ],
};
