from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
import requests
from rest_framework_simplejwt import views as jwt_views
admin.site.site_header = "ሺመላ የውኃ ቢል አስተዳዳሪ"
admin.site.site_title = "DWBS"
admin.site.index_title = "Welcome to DWBS"
from django.conf import settings

from django.conf.urls.static import static
# from student.views import dashboard_view
urlpatterns = [
    # path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),  # Default Django admin
    path('chaining/', include('smart_selects.urls')),
    path('', include('dashboard.urls')),
    # path('', dashboard_view, name='dashboard'),  # Route the root URL to the dashboard view
    path('api/', include('reads.urls')),
    path('api/', include('bills.urls')), 
    path('employees/', include('employees.urls')),  # Include employees URLs here
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('student/', include('student.urls')),  # Include student app URLs
    # path('', include('student.urls')), 
   
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

