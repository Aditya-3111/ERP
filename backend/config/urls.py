from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core & Auth APIs
    path('api/auth/', include('apps.core.api.auth_urls')),
    path('api/core/', include('apps.core.api.urls')),
    
    # Module APIs
    path('api/finance/', include('apps.finance.api.urls')),
    path('api/inventory/', include('apps.inventory.api.urls')),
    path('api/crm/', include('apps.crm.api.urls')),
    path('api/hr/', include('apps.hr.api.urls')),
    path('api/gate/', include('apps.gate.api.urls')),
    path('api/pos/', include('apps.pos.api.urls')),
    path('api/production/', include('apps.production.api.urls')),
    path('api/maintenance/', include('apps.maintenance.api.urls')),
    path('api/admin/', include('apps.admin_panel.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)