from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Q
from apps.admin_panel.models import (
    RegisteredModule, ModuleSetting, MenuGroup, MenuItem,
    PermissionGroup, Permission, RolePermission, UserPermission,
    ThemeSettings
)
from apps.admin_panel.api.serializers import (
    RegisteredModuleSerializer, ModuleSettingSerializer,
    MenuGroupSerializer, MenuItemSerializer,
    PermissionGroupSerializer, PermissionSerializer,
    RolePermissionSerializer, UserPermissionSerializer,
    ThemeSettingsSerializer
)


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin users"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and
                    (request.user.is_superuser or
                     (hasattr(request.user, 'role') and
                      request.user.role and
                      request.user.role.name in ['admin', 'administrator'])))


# ============================================
# Module Registry
# ============================================
class RegisteredModuleViewSet(viewsets.ModelViewSet):
    queryset = RegisteredModule.objects.all()
    serializer_class = RegisteredModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = RegisteredModule.objects.all()
        is_active = self.request.query_params.get('is_active')
        module_key = self.request.query_params.get('module_key')
        if is_active is not None:
            qs = qs.filter(is_active=is_active)
        if module_key:
            qs = qs.filter(module_key=module_key)
        return qs.order_by('sort_order')


class ModuleSettingViewSet(viewsets.ModelViewSet):
    queryset = ModuleSetting.objects.all()
    serializer_class = ModuleSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ModuleSetting.objects.all()
        module = self.request.query_params.get('module')
        if module:
            qs = qs.filter(module__guid=module)
        return qs


# ============================================
# Menu Management
# ============================================
class MenuGroupViewSet(viewsets.ModelViewSet):
    queryset = MenuGroup.objects.all()
    serializer_class = MenuGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = MenuGroup.objects.filter(is_active=True)
        user = self.request.user
        # Filter by role if not admin
        if user.role and user.role.name not in ['admin', 'administrator']:
            role_perms = RolePermission.objects.filter(role=user.role, access_level__in=['read', 'write', 'delete', 'full'])
            permitted_modules = role_perms.values_list('permission__module__module_key', flat=True)
            qs = qs.filter(items__required_permission__in=permitted_modules) | qs.filter(items__required_permission='')
        return qs.distinct().order_by('sort_order')


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]


# ============================================
# Permissions
# ============================================
class PermissionGroupViewSet(viewsets.ModelViewSet):
    queryset = PermissionGroup.objects.all()
    serializer_class = PermissionGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = Permission.objects.all()
        group = self.request.query_params.get('group')
        module = self.request.query_params.get('module')
        if group:
            qs = qs.filter(permission_group__guid=group)
        if module:
            qs = qs.filter(module__guid=module)
        return qs


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = RolePermission.objects.all()
        role = self.request.query_params.get('role')
        if role:
            qs = qs.filter(role__guid=role)
        return qs.select_related('role', 'permission')


class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        qs = UserPermission.objects.all()
        user = self.request.query_params.get('user')
        if user:
            qs = qs.filter(user__guid=user)
        return qs


# ============================================
# Theme Settings
# ============================================
class ThemeSettingsViewSet(viewsets.ModelViewSet):
    queryset = ThemeSettings.objects.all()
    serializer_class = ThemeSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ThemeSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============================================
# Role-based Menu API (returns menu for current user)
# ============================================
class MenuForCurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = MenuGroup.objects.filter(is_active=True).order_by('sort_order')
        data = []
        for group in groups:
            items = MenuItem.objects.filter(group=group, is_active=True).order_by('sort_order')
            # Filter items by role permission
            if user.role and user.role.name not in ['admin', 'administrator']:
                role_perms = RolePermission.objects.filter(
                    role=user.role,
                    access_level__in=['read', 'write', 'delete', 'full']
                ).values_list('permission__permission_key', flat=True)
                items = items.filter(
                    Q(required_permission='') | Q(required_permission__in=role_perms)
                )
            if items.exists():
                data.append({
                    'guid': group.guid,
                    'group_key': group.group_key,
                    'group_label': group.group_label,
                    'group_icon': group.group_icon,
                    'items': [{
                        'guid': item.guid,
                        'item_key': item.item_key,
                        'item_label': item.item_label,
                        'item_icon': item.item_icon,
                        'item_page': item.item_page,
                        'item_url': item.item_url,
                        'badge_text': item.badge_text,
                        'badge_color': item.badge_color,
                    } for item in items]
                })
        return Response(data)
