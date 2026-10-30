from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .dashboard import DashboardView
from rest_framework_simplejwt.views import TokenRefreshView
from apps.core.api.views import (
    LoginView, LogoutView, ChangePasswordView, ProfileView,
    UserViewSet, FinancialYearViewSet, CompanyProfileViewSet,
    BranchViewSet, RoleViewSet, SystemSettingViewSet,
    AuditLogViewSet,
)
from apps.core.api.notifications import NotificationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'financial-years', FinancialYearViewSet, basename='financial-year')
router.register(r'company-profiles', CompanyProfileViewSet, basename='company-profile')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'settings', SystemSettingViewSet, basename='setting')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

urlpatterns += router.urls