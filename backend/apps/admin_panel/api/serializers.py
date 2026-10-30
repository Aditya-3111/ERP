from rest_framework import serializers
from apps.admin_panel.models import (
    RegisteredModule, ModuleSetting, MenuGroup, MenuItem,
    PermissionGroup, Permission, RolePermission, UserPermission,
    ThemeSettings
)


class RegisteredModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredModule
        fields = '__all__'
        read_only_fields = ['guid', 'created_at', 'updated_at']


class ModuleSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleSetting
        fields = '__all__'
        read_only_fields = ['guid', 'created_at', 'updated_at']


class MenuGroupSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = MenuGroup
        fields = '__all__'
        read_only_fields = ['guid', 'created_at', 'updated_at']

    def get_items(self, obj):
        items = obj.items.filter(is_active=True).order_by('sort_order')
        return MenuItemSerializer(items, many=True).data


class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['guid', 'created_at', 'updated_at']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('sort_order')
        return MenuItemSerializer(children, many=True).data


class PermissionGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = PermissionGroup
        fields = '__all__'
        read_only_fields = ['guid', 'created_at']

    def get_permissions(self, obj):
        perms = obj.permissions.all()
        return PermissionSerializer(perms, many=True).data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        read_only_fields = ['guid', 'created_at']


class RolePermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.label', read_only=True)
    permission_name = serializers.CharField(source='permission.permission_name', read_only=True)
    permission_key = serializers.CharField(source='permission.permission_key', read_only=True)

    class Meta:
        model = RolePermission
        fields = '__all__'
        read_only_fields = ['guid', 'granted_at']


class UserPermissionSerializer(serializers.ModelSerializer):
    permission_name = serializers.CharField(source='permission.permission_name', read_only=True)

    class Meta:
        model = UserPermission
        fields = '__all__'
        read_only_fields = ['guid', 'granted_at']


class ThemeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSettings
        fields = '__all__'
        read_only_fields = ['guid', 'updated_at']


class MenuForRoleSerializer(serializers.Serializer):
    """Returns menu structure filtered by user role permissions"""
    groups = MenuGroupSerializer(many=True)
