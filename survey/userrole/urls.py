from django.urls import path

from . import views
app_name = 'userrole'

urlpatterns = [
        path('assign-project-manager/<int:project_id>/', views.AssignProjectManagerView.as_view(), name="userrole_create"),
        path('assign-engineer/<int:site_id>/', views.FieldEngineerUserRoleFormView.as_view(), name="assign_field_engineer"),
        path('field-engineer-create/<int:project_id>/', views.FieldEngineerCreate.as_view(), name="field_engineer_create"),
        # path('field-engineer-delete/<int:project_id>/', views.FieldEngineerDelete.as_view(), name="field_engineer_delete"),
        path('project-user-create/<int:project_id>/', views.ProjectUserFormView.as_view(), name="project_user_create"),
        path('project-user-list/<int:project_id>/', views.ProjectUserListView.as_view(), name="project_user_list"),
        path('email-invitation/<int:project_id>/', views.SendInvitationView.as_view(), name="send_invitation"),
        path('thank-you/', views.Thankyou.as_view(), name="thankyou"),
        path('role-delete/<int:pk>', views.RoleDelete.as_view(), name="role_delete"),
        path('project-manager-edit/<int:pk>', views.AssignProjectManagerPhoneNumber.as_view(), name="assign_phone_number"),

]