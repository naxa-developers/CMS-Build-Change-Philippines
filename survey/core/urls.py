from django.urls import path

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
    path('site-create/<int:project_id>/', views.SiteCreateView.as_view(), name="site_create"),
    path('site-update/<int:pk>/', views.SiteUpdateView.as_view(), name="site_update"),
    path('site-list/', views.SiteListView.as_view(), name="site_list"),
    path('site-delete/<int:pk>/', views.SiteDeleteView.as_view(), name="site_delete"),
    path('site-detail/<int:pk>/', views.SiteDetailView.as_view(), name="site_detail"),
    path('steps/<int:is_project>/<int:pk>/', views.SiteStepsView.as_view(), name="site-steps"),
    path('category-create/<int:project_id>/', views.CategoryFormView.as_view(), name="category_create"),
    path('category-update/<int:pk>', views.CategoryUpdateView.as_view(), name="category_update"),
    path('category-delete/<int:pk>', views.CategoryDeleteView.as_view(), name="category_delete"),
    path('material-create/<int:project_id>/', views.MaterialFormView.as_view(), name="material_create"),
    path('material-update/<int:pk>/', views.MaterialUpdateView.as_view(), name="material_update"),
    path('material-delete/<int:pk>/', views.MaterialDeleteView.as_view(), name="material_delete"),
]