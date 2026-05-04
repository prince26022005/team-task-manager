from django.contrib import admin
from django.urls import path, include
from core.views import login_page, dashboard, signup_page, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ye home/auth pages hain
    path('', login_page),
    path('dashboard/', dashboard),
    path('signup/', signup_page),
    path('login/', login_view),
    
    # Sirf yaha 'projects/' likho, baaki kahin nahi
    path('projects/', include('core.urls')),
]