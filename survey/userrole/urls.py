from django.urls import path

from . import views
app_name = 'userrole'

urlpatterns = [
    path('userrole-create/<int:project_id>/', views.UserRoleCreateView.as_view(), name="userrole_create"),

]