from django.contrib.auth.models import User

from rest_framework import viewsets, serializers

from core.models import Project
from .serializers import ProjectSerializer


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('sites', 'sites__steps')