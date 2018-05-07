from django.urls import path

from . import views

urlpatterns = [
    path('project-create/', views.ProjectCreateView.as_view()),
    path('project-list/', views.ProjectListView.as_view()),
    path('project-detail/<int:pk>/', views.ProjectDetailView.as_view()),
    path('project-update/<int:pk>/', views.ProjectUpdateView.as_view()),
    path('project-delete/<int:pk>/', views.ProjectDeleteView.as_view())

]