from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin-api/', admin.site.urls),
    #! honeypot admin for attacks on admin panel
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    path('', include('dashboard.urls', namespace='dashboard')),

]