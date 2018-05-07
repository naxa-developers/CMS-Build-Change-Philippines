from django.urls import path, include

from rest_framework import routers

from . import viewset
from .. import views

router = routers.DefaultRouter()

router.register(r'users', viewset.UserViewSet)
router.register(r'project', viewset.ProjectViewSet, base_name='project-list')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.token),

]