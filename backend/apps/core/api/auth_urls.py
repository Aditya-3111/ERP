from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.core.api.views import LoginView, LogoutView, ChangePasswordView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
