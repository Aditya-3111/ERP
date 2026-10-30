import calendar
from datetime import date as _date
from decimal import Decimal
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.hr.models import Department, Designation, Employee, Attendance, PayHead, EmployeeDocument
from .serializers import (DepartmentSerializer, DesignationSerializer, 
                           EmployeeSerializer, AttendanceSerializer,
                           PayHeadSerializer, EmployeeDocumentSerializer)
from rest_framework.permissions import IsAuthenticated

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['is_active']
    ordering_fields = ['name']
    ordering = ['name']

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'department__name']
    filterset_fields = ['department']
    ordering_fields = ['name']
    ordering = ['name']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['emp_code', 'name', 'mobile', 'email']
    filterset_fields = ['department', 'designation', 'status', 'gender']
    ordering_fields = ['emp_code', 'name', 'date_of_joining']
    ordering = ['emp_code']

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['employee__name']
    filterset_fields = ['employee', 'date', 'status']
    ordering_fields = ['date', 'in_time']
    ordering = ['-date']

    # status values the HTML pages send -> values stored in the database
    STATUS_MAP = {
        'present': ('Present', ''), 'absent': ('Absent', ''),
        'late': ('Present', 'Late'), 'half-day': ('Half Day', ''),
        'half day': ('Half Day', ''), 'leave': ('Leave', ''),
        'holiday': ('Holiday', ''),
    }

    @action(detail=False, methods=['post'])
    def bulk(self, request):
        """POST /api/hr/attendance/bulk/
        Body: {"attendances": [{"employee": guid, "date": "YYYY-MM-DD",
               "status": "present|absent|late|half-day", "check_in": "09:00",
               "check_out": "18:00"}, ...]}
        Creates or updates one attendance row per employee per day."""
        rows = request.data.get('attendances')
        if not isinstance(rows, list) or not rows:
            return Response({'error': 'attendances (non-empty list) is required'}, status=400)
        created = updated = 0
        errors = []
        with transaction.atomic():
            for i, row in enumerate(rows):
                try:
                    emp = Employee.objects.get(pk=row.get('employee'))
                    status_name, remark = self.STATUS_MAP.get(
                        str(row.get('status', 'present')).lower(),
                        (row.get('status') or 'Present', ''))
                    defaults = {
                        'status': status_name,
                        'in_time': row.get('check_in') or row.get('in_time') or None,
                        'out_time': row.get('check_out') or row.get('out_time') or None,
                        'remarks': row.get('remarks') or remark,
                    }
                    if status_name in ('Absent', 'Leave', 'Holiday'):
                        defaults['in_time'] = defaults['out_time'] = None
                    _, was_created = Attendance.objects.update_or_create(
                        employee=emp, date=row.get('date'), defaults=defaults)
                    created += was_created
                    updated += (not was_created)
                except Exception as exc:  # report the bad row, keep the others
                    errors.append({'row': i, 'error': str(exc)})
        return Response({'created': created, 'updated': updated, 'errors': errors},
                        status=status.HTTP_200_OK if not errors else status.HTTP_207_MULTI_STATUS)

class PayHeadViewSet(viewsets.ModelViewSet):
    queryset = PayHead.objects.all()
    serializer_class = PayHeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['pay_type', 'income_type']
    ordering_fields = ['name']
    ordering = ['name']

class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDocument.objects.all()
    serializer_class = EmployeeDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['employee__name', 'document_type', 'document_name']
    filterset_fields = ['employee', 'document_type']
    ordering_fields = ['uploaded_at', 'document_type']
    ordering = ['-uploaded_at']



class PayrollSummaryView(APIView):
    """GET /api/hr/payroll/?month=YYYY-MM&department=Name

    Simple derived payroll: basic = employee.salary; deduction = one day's pay
    (salary / days in month) for every Absent day and half a day's pay for
    every Half Day recorded in that month. There is no payslip table yet."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month') or _date.today().strftime('%Y-%m')
        try:
            year, mon = [int(x) for x in month.split('-')[:2]]
            days_in_month = calendar.monthrange(year, mon)[1]
        except (ValueError, IndexError):
            return Response({'error': 'month must be YYYY-MM'}, status=400)

        employees = Employee.objects.filter(status='active')
        dept = request.query_params.get('department')
        if dept:
            employees = employees.filter(department__iexact=dept)

        result = []
        for emp in employees.order_by('emp_code'):
            att = Attendance.objects.filter(employee=emp, date__year=year, date__month=mon)
            absent = att.filter(status='Absent').count()
            half = att.filter(status='Half Day').count()
            basic = Decimal(emp.salary or 0)
            per_day = basic / Decimal(days_in_month)
            deductions = (per_day * Decimal(absent + half * Decimal('0.5'))).quantize(Decimal('0.01'))
            result.append({
                'employee': emp.guid, 'emp_code': emp.emp_code,
                'employee_name': emp.name, 'department': emp.department,
                'month': month, 'days_in_month': days_in_month,
                'absent_days': absent, 'half_days': half,
                'basic': float(basic), 'allowances': 0.0,
                'deductions': float(deductions),
                'net_salary': float(basic - deductions),
                'status': 'pending',
            })
        return Response({'count': len(result), 'results': result})
