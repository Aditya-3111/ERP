from rest_framework import serializers
from apps.hr.models import Department, Designation, Employee, Attendance, PayHead, EmployeeDocument
import uuid

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['guid', 'name', 'description', 'is_active']
        read_only_fields = ['guid']

class DesignationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Designation
        fields = ['guid', 'name', 'department', 'department_name', 'description']
        read_only_fields = ['guid']

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['guid', 'emp_code', 'name', 'department', 'department_name', 
                 'designation', 'designation_name', 'function_role', 
                 'location', 'gender', 'date_of_birth', 'blood_group',
                 'father_mother_name', 'spouse_name', 'address', 'city', 
                 'state', 'pincode', 'mobile', 'email', 
                 'pan', 'aadhaar', 'uan', 'pf_number', 
                 'date_of_joining', 'date_of_release', 'salary', 'status',
                 'photo', 'remarks']
        read_only_fields = ['guid']

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['guid', 'employee', 'employee_name', 'date', 'in_time', 
                 'out_time', 'status', 'remarks']
        read_only_fields = ['guid']

class PayHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayHead
        fields = ['guid', 'name', 'parent', 'payslip_name', 'pay_type',
                 'income_type', 'calculation_type', 'leave_type', 'calculation_period']
        read_only_fields = ['guid']

class EmployeeDocumentSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    
    class Meta:
        model = EmployeeDocument
        fields = ['guid', 'employee', 'employee_name', 'document_type',
                 'document_name', 'document_file', 'uploaded_at']
        read_only_fields = ['guid', 'uploaded_at']
