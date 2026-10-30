from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.core.models import (
    FinancialYear, CompanyProfile, Branch, Role, SystemSetting, AuditLog
)
from apps.admin_panel.models import Notification

User = get_user_model()


# ============================================
# User & Auth Serializers
# ============================================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)
    role_name = serializers.CharField(source='role.label', read_only=True)
    role_code = serializers.SerializerMethodField()   # e.g. 'admin', 'accountant' (used by the React menu)
    fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'guid', 'username', 'password', 'email', 'first_name', 'last_name',
            'fullname', 'mobile', 'role', 'role_name', 'role_code', 'status', 'avatar',
            'is_active', 'is_superuser', 'date_joined', 'last_login'
        ]
        read_only_fields = ['guid', 'date_joined', 'last_login', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_fullname(self, obj):
        return obj.get_full_name()

    def get_role_code(self, obj):
        return obj.role.name if obj.role else ''
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.label', read_only=True)
    fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['guid', 'username', 'email', 'fullname', 'mobile', 'role_name', 'status', 'is_active']
    
    def get_fullname(self, obj):
        return obj.get_full_name()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    financial_year_guid = serializers.UUIDField(required=False)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)


# ============================================
# Core Model Serializers
# ============================================
class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = '__all__'
        read_only_fields = ['guid', 'created_at']


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['guid', 'created_at', 'updated_at']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ['guid', 'created_at']


class RoleSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['guid', 'name', 'label', 'description', 'is_system', 'user_count', 'created_at']
        read_only_fields = ['guid', 'created_at']
    
    def get_user_count(self, obj):
        return User.objects.filter(role=obj).count()


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = '__all__'
        read_only_fields = ['guid']


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='username', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['guid', 'user', 'user_name', 'action', 'module', 'details', 'ip_address', 'created_at']
        read_only_fields = ['guid', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['guid', 'user', 'notification_type', 'title', 'message', 'link', 'is_read', 'read_at', 'created_at']
        read_only_fields = ['guid', 'created_at']


# ============================================
# Dashboard Serializers
# ============================================
