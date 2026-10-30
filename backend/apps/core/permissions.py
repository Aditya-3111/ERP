from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin/administrator role users"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'role') and request.user.role:
            return request.user.role.name in ['admin', 'administrator']
        return False


class IsRoleUser(permissions.BasePermission):
    """Allow access based on allowed role names"""
    allowed_roles = []

    def __init__(self, allowed_roles=None):
        if allowed_roles is not None:
            self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'role') and request.user.role:
            return request.user.role.name in self.allowed_roles
        return False


class IsAccountant(IsRoleUser):
    def __init__(self):
        super().__init__(allowed_roles=['admin', 'administrator', 'accountant', 'accounts'])


class IsSalesUser(IsRoleUser):
    def __init__(self):
        super().__init__(allowed_roles=['admin', 'administrator', 'sales', 'salesman'])


class IsStoreUser(IsRoleUser):
    def __init__(self):
        super().__init__(allowed_roles=['admin', 'administrator', 'store', 'storekeeper'])


class IsHRUser(IsRoleUser):
    def __init__(self):
        super().__init__(allowed_roles=['admin', 'administrator', 'hr', 'hr_manager'])


class IsGateUser(IsRoleUser):
    def __init__(self):
        super().__init__(allowed_roles=['admin', 'administrator', 'gate', 'security'])


def get_user_dashboard(user):
    """Returns the default dashboard page based on user role"""
    if not user or not hasattr(user, 'role') or not user.role:
        return 'dashboard'
    role_map = {
        'admin': 'dashboard',
        'administrator': 'dashboard',
        'accountant': 'dashboard-finance',
        'accounts': 'dashboard-finance',
        'sales': 'dashboard-crm',
        'salesman': 'dashboard-crm',
        'store': 'dashboard-store',
        'storekeeper': 'dashboard-store',
        'hr': 'dashboard-hr',
        'hr_manager': 'dashboard-hr',
        'gate': 'dashboard-gate',
        'security': 'dashboard-gate',
    }
    return role_map.get(user.role.name, 'dashboard')
