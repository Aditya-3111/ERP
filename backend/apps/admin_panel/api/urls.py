from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.admin_panel.api.views import (
    RegisteredModuleViewSet, ModuleSettingViewSet,
    MenuGroupViewSet, MenuItemViewSet,
    PermissionGroupViewSet, PermissionViewSet,
    RolePermissionViewSet, UserPermissionViewSet,
    ThemeSettingsViewSet, MenuForCurrentUserView
)

router = DefaultRouter()
router.register(r'modules', RegisteredModuleViewSet, basename='admin-module')
router.register(r'module-settings', ModuleSettingViewSet, basename='admin-module-setting')
router.register(r'menu-groups', MenuGroupViewSet, basename='admin-menu-group')
router.register(r'menu-items', MenuItemViewSet, basename='admin-menu-item')
router.register(r'permission-groups', PermissionGroupViewSet, basename='admin-permission-group')
router.register(r'permissions', PermissionViewSet, basename='admin-permission')
router.register(r'role-permissions', RolePermissionViewSet, basename='admin-role-permission')
router.register(r'user-permissions', UserPermissionViewSet, basename='admin-user-permission')
router.register(r'themes', ThemeSettingsViewSet, basename='admin-theme')

urlpatterns = [
    path('menu/', MenuForCurrentUserView.as_view(), name='admin-menu-current-user'),
]

urlpatterns += router.urls
