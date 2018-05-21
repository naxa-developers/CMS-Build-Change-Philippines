from django.urls import path

from . import views
app_name = 'userrole'

urlpatterns = [
        path('assign-project-manager/<int:project_id>/', views.UserRoleCreateView.as_view(), name="userrole_create"),
        path('assign-engineer/<int:site_id>/', views.FieldEngineerUserRoleFormView.as_view(), name="field_engineer_create"),
        path('project-user-create/<int:project_id>/', views.ProjectUserFormView.as_view(), name="project_user_create"),
        path('project-user-list/<int:project_id>/', views.ProjectUserListView.as_view(), name="project_user_list"),

]