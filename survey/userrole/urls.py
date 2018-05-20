from django.urls import path

from . import views
app_name = 'userrole'

urlpatterns = [
        path('userrole-create/<int:project_id>/', views.UserRoleCreateView.as_view(), name="userrole_create"),
        path('field-engineer-create/<int:site_id>/', views.FieldEngineerUserRoleFormView.as_view(), name="field_engineer_create"),

]