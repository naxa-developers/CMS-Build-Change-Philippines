from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('project-create/', views.ProjectCreateView.as_view(), name="project_create"),
    # path('project-detail/<int:pk>/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project-update/<int:pk>/', views.ProjectUpdateView.as_view(), name="project_update"),
    path('project-delete/<int:pk>/', views.ProjectDeleteView.as_view(), name="project_delete"),
    path('user-create/', views.UserCreateView.as_view(), name="user_create"),
    path('user-list/', views.UserListView.as_view(), name="user_list"),
    path('dashboard/', views.Dashboard.as_view(), name="admin_dashboard"),
    path('project-dashboard/<int:project_id>', views.ProjectDashboard.as_view(), name="project_dashboard"),
    path('site-create/<int:project_id>/', views.SiteCreateView.as_view(), name="site_create"),
    path('site-update/<int:pk>/', views.SiteUpdateView.as_view(), name="site_update"),
    path('site-list/', views.SiteListView.as_view(), name="site_list"),
    path('site-delete/<int:pk>/', views.SiteDeleteView.as_view(), name="site_delete"),
    path('site-detail/<int:pk>/', views.SiteDetailView.as_view(), name="site_detail"),
    path('site-detail-js/<int:site_pk>/', views.SiteDetailTemplateView.as_view(), name="site_detail_js"),
    path('steps/<int:is_project>/<int:pk>/', views.SiteStepsView.as_view(), name="site-steps"),
    path('category-create/<int:project_id>/', views.CategoryFormView.as_view(), name="category_create"),
    path('category-list/<int:project_id>', views.CategoryListView.as_view(), name="category_list"),
    path('category-update/<int:pk>', views.CategoryUpdateView.as_view(), name="category_update"),
    path('category-delete/<int:pk>', views.CategoryDeleteView.as_view(), name="category_delete"),
    path('guideline-create/<int:project_id>/', views.MaterialFormView.as_view(), name="material_create"),
    path('guideline-update/<int:pk>/', views.MaterialUpdateView.as_view(), name="material_update"),
    path('guideline-delete/<int:pk>/', views.MaterialDeleteView.as_view(), name="material_delete"),
    path('guideline-detail/<int:pk>', views.MaterialDetailView.as_view(), name="material_detail"),
    path('guideline-list/<int:pk>', views.MaterialListView.as_view(), name="material_list"),
    path('site-guideline-create/<int:site_id>/', views.SiteMaterialFormView.as_view(), name="site_material_create"),
    path('site-guideline-list/<int:site_id>/', views.SiteMaterialListView.as_view(), name="site_material_list"),
    path('site-guideline-detail/<int:pk>/', views.SiteMaterialDetailView.as_view(), name="site_material_detail"),
    path('site-guideline-delete/<int:pk>/', views.SiteMaterialDeleteView.as_view(), name="site_material_delete"),
    path('document-create/<int:site_id>/', views.SiteDocumentFormView.as_view(), name="document_create"),
    path('document-list/<int:site_id>/', views.SiteDocumentListView.as_view(), name="document_list"),
    path('document-delete/<int:pk>/', views.SiteDocumentDeleteView.as_view(), name="document_delete"),
    path('site-report-list/<int:site_pk>', views.ReportListView.as_view(), name="report_list"),
    path('report-detail/<int:pk>', views.ReportDetailView.as_view(), name="report_detail"),
    path('user-profile-create/<int:pk>', views.UserProfileView.as_view(), name="user_profile"),
    path('user-profile-update/<int:pk>', views.	UserProfileUpdateView.as_view(), name="user_profile_update"),
    path('user-profile-detail/<int:pk>', views.UserProfileDetailView.as_view(), name="user_profile_detail"),
]

