from django.urls import path, include

from rest_framework import routers

from . import viewset
from .. import views
from core.viewsets import StepViewset
router = routers.DefaultRouter()

router.register(r'users', viewset.UserViewSet)
router.register(r'project', viewset.ProjectViewSet, base_name='project-list')
router.register(r'steps', viewset.StepsViewSet, base_name='steps-list')
router.register(r'checklist', StepViewset.ChecklistViewset, base_name='checklist-api')
router.register(r'step', StepViewset.ChecklistViewset, base_name='step-api')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.token),
    path('list-steps/<int:is_project>/<int:pk>/',
         viewset.ProjectSiteStepsViewSet.as_view({'get':  'list'})),
    path('step-list/<int:pk>/', StepViewset.StepViewset.as_view({'get': 'list',}), name="api_steps"),
    path('checklist-list/<int:pk>/', StepViewset.ChecklistViewset.as_view({'get': 'list',}), name="api_checklist"),


]