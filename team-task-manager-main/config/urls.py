from django.contrib import admin
from django.urls import path, include
from core.views import login_page
from core.views import  dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),

    path('', login_page),
    path('dashboard/', dashboard),
    path('', include('core.urls')), 

]