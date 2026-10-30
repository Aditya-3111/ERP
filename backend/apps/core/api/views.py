from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from apps.core.models import (
    FinancialYear, CompanyProfile, Branch, Role, SystemSetting, AuditLog
)
from apps.core.api.serializers import (
    UserSerializer, UserListSerializer, LoginSerializer, TokenSerializer,
    ChangePasswordSerializer, FinancialYearSerializer, CompanyProfileSerializer,
    BranchSerializer, RoleSerializer, SystemSettingSerializer, AuditLogSerializer,
    
)
from apps.core.permissions import get_user_dashboard

User = get_user_model()


# ============================================
# Base CRUD ViewSet (Reusable)
# ============================================
class BaseCRUDViewSet(viewsets.ModelViewSet):
    """Base ViewSet with common CRUD functionality"""
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
        self.log_action('CREATE', serializer.instance)
    
    def perform_update(self, serializer):
        serializer.save()
        self.log_action('UPDATE', serializer.instance)
    
    def perform_destroy(self, instance):
        self.log_action('DELETE', instance)
        instance.delete()
    
    def log_action(self, action, instance):
        AuditLog.objects.create(
            user=self.request.user,
            username=self.request.user.username,
            action=action,
            module=self.__class__.__name__,
            details=f"{action} {instance}"
        )
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export data as CSV"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ============================================
# Authentication Views
# ============================================
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        
        # Set financial year if provided
        fy_guid = serializer.validated_data.get('financial_year_guid')
        if fy_guid:
            try:
                fy = FinancialYear.objects.get(guid=fy_guid)
                user.financial_year = fy
                user.save(update_fields=['financial_year'])
            except FinancialYear.DoesNotExist:
                pass
        
        # Log audit
        AuditLog.objects.create(
            user=user,
            username=user.username,
            action='LOGIN',
            module='Auth',
            details=f"User {username} logged in"
        )
        
        user_data = UserSerializer(user).data
        user_data['default_dashboard'] = get_user_dashboard(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_data
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            AuditLog.objects.create(
                user=request.user,
                username=request.user.username,
                action='LOGOUT',
                module='Auth',
                details=f"User {request.user.username} logged out"
            )
        except Exception:
            pass
        
        return Response({'message': 'Logged out successfully'})


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ============================================
# User Management ViewSet
# ============================================
class UserViewSet(BaseCRUDViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search')
        role = self.request.query_params.get('role')
        status = self.request.query_params.get('status')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        if role:
            queryset = queryset.filter(role__name=role)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-date_joined')
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        user = self.get_object()
        user.status = 'inactive' if user.status == 'active' else 'active'
        user.save()
        return Response({'status': user.status})
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('new_password', 'Password@123')
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully'})


# ============================================
# Core Model ViewSets
# ============================================
class FinancialYearViewSet(BaseCRUDViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        FinancialYear.objects.update(is_active=False)
        fy = self.get_object()
        fy.is_active = True
        fy.save()
        return Response({'message': f'{fy.name} set as active'})


class CompanyProfileViewSet(BaseCRUDViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer


class BranchViewSet(BaseCRUDViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class RoleViewSet(BaseCRUDViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class SystemSettingViewSet(BaseCRUDViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    
    @action(detail=False, methods=['get'])
    def by_key(self, request):
        key = request.query_params.get('key')
        if key:
            setting = SystemSetting.objects.filter(key=key).first()
            if setting:
                return Response(SystemSettingSerializer(setting).data)
        return Response({'error': 'Key not found'}, status=404)


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = AuditLog.objects.all()
        module = self.request.query_params.get('module')
        user_id = self.request.query_params.get('user_id')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if module:
            queryset = queryset.filter(module=module)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())[:100]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ============================================
# Dashboard View
# ============================================
