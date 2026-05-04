from django.urls import path
from .views import *
from .views import add_task
from . import views

urlpatterns = [
    path('', login_page),
    path('signup/', signup_page),

    path('login/', login_view),
    path('register/', register),

    path('dashboard/', dashboard),

    path('projects/', projects_page),
    path('projects/<int:id>/', project_detail),

    path('projects/create/', create_project),
    path('projects/<int:id>/delete/', delete_project),
    path('projects/<int:id>/add-member/', add_member),

    path('projects/<int:id>/add-task/', add_task),

    path('tasks/<int:id>/update/', update_task_status),
    path('tasks/<int:id>/delete/', delete_task),

    path('api/', home),

    path('projects/<int:id>/add-member/', views.add_member),
    path('projects/<int:id>/delete/', views.delete_project),
    path('projects/<int:id>/add-task/', views.add_task),
]