from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_page, name='projects_page'),
    path('create/', views.create_project, name='create_project'),
    path('<int:id>/', views.project_detail, name='project_detail'),
    path('<int:id>/delete/', views.delete_project, name='delete_project'),
    path('<int:id>/add-member/', views.add_member, name='add_member'),
    path('<int:id>/add-task/', views.add_task, name='add_task'),
    
    # Tasks ke liye alag path
    path('tasks/<int:id>/update/', views.update_task_status, name='update_task'),
    path('tasks/<int:id>/delete/', views.delete_task, name='delete_task'),
]