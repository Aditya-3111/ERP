from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DepartmentViewSet, DesignationViewSet, EmployeeViewSet,
                       AttendanceViewSet, PayHeadViewSet, 
                       EmployeeDocumentViewSet, PayrollSummaryView)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'designations', DesignationViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'payheads', PayHeadViewSet)
router.register(r'documents', EmployeeDocumentViewSet)

urlpatterns = [
    path('payroll/', PayrollSummaryView.as_view(), name='payroll-summary'),
    path('', include(router.urls)),
]
