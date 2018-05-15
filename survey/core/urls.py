from django.urls import path
from .viewsets import StepViewset
from . import views
app_name = 'core'

urlpatterns = [
    path('project-create/', views.ProjectCreateView.as_view(), name="project_create"),
    path('project-detail/<int:pk>/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project-update/<int:pk>/', views.ProjectUpdateView.as_view(), name="project_update"),
    path('project-delete/<int:pk>/', views.ProjectDeleteView.as_view(), name="project_delete"),

    path('user-create/', views.UserCreateView.as_view(), name="user_create"),
    path('dashboard/', views.Dashboard.as_view(), name="admin_dashboard"),
    path('project-dashboard/', views.ProjectDashboard.as_view(), name="project_dashboard"),
    path('site-create/<int:pk>/', views.SiteCreateView.as_view(), name="site_create"),
    path('site-update/<int:pk>/', views.SiteUpdateView.as_view(), name="site_update"),
    path('site-list/', views.SiteListView.as_view(), name="site_list"),
    path('site-delete/<int:pk>/', views.SiteDeleteView.as_view(), name="site_delete"),

    path('site/<int:pk>/steps/', StepViewset.StepViewset.as_view({'get': 'list', 'post':'create'}), name="api_steps"),
    path('site/<int:site_id>/step/<int:pk>/checklists/', StepViewset.ChecklistViewset.as_view({'get': 'list', 'post':'create'}), name="api_steps"),

    path('site-detail/<int:pk>/', views.SiteDetailView.as_view(), name="site_detail"),
    path('steps/<int:is_project>/<int:pk>/', views.SiteStepsView.as_view(), name="site-steps")
]