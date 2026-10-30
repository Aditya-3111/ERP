"""Attendance, payroll, employee documents."""
import uuid

from apps.hr.models import Attendance, Employee

from tests.base import BaseAPITest


class HRTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.emp = Employee.objects.create(emp_code='E1', name='Ravi', department='Sales', salary=30000)

    def test_bulk_attendance_creates_then_updates(self):
        row = {'employee': str(self.emp.guid), 'date': '2026-03-02', 'status': 'late',
               'check_in': '09:40', 'check_out': '18:00'}
        r = self.client.post('/api/hr/attendance/bulk/', {'attendances': [row]}, format='json')
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.json()['created'], 1)
        att = Attendance.objects.get(employee=self.emp)
        self.assertEqual((att.status, att.remarks), ('Present', 'Late'))
        row['status'] = 'absent'
        r = self.client.post('/api/hr/attendance/bulk/', {'attendances': [row]}, format='json')
        self.assertEqual(r.json()['updated'], 1)
        self.assertEqual(Attendance.objects.get(employee=self.emp).status, 'Absent')

    def test_bulk_attendance_reports_bad_rows(self):
        r = self.client.post('/api/hr/attendance/bulk/',
                             {'attendances': [{'employee': str(uuid.uuid4()), 'date': '2026-03-02'}]}, format='json')
        self.assertEqual(r.status_code, 207)
        self.assertEqual(len(r.json()['errors']), 1)

    def test_payroll_deducts_absent_days(self):
        Attendance.objects.create(employee=self.emp, date='2026-03-02', status='Absent')
        r = self.client.get('/api/hr/payroll/?month=2026-03')
        self.assertEqual(r.status_code, 200)
        p = r.json()['results'][0]
        self.assertEqual(p['basic'], 30000.0)
        self.assertEqual(p['deductions'], 967.74)         # 30000 / 31 days
        self.assertAlmostEqual(p['net_salary'], 30000 - 967.74, places=2)

    def test_employee_documents_endpoint_no_longer_500(self):
        self.assertEqual(self.client.get('/api/hr/documents/').status_code, 200)
