from django.urls import path

from . import views
app_name = 'core'

urlpatterns = [
    path('project-create/', views.ProjectCreateView.as_view(), name="project_create"),
    path('project-list/', views.ProjectListView.as_view(), name="project_list"),
    path('project-detail/<int:pk>/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project-update/<int:pk>/', views.ProjectUpdateView.as_view(), name="project_update"),
    path('project-delete/<int:pk>/', views.ProjectDeleteView.as_view(), name="project_delete"),

]