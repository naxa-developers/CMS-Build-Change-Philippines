from django.contrib.auth.models import User

from rest_framework import viewsets, serializers, mixins

from core.models import Project, Step
from .serializers import ProjectSerializer, StepsSerializer


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


class ProjectSiteStepsViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = StepsSerializer
    queryset = Step.objects.all()

    def get_queryset(self):
        is_project = self.kwargs['is_project']
        pk = self.kwargs['pk']

        if is_project == 1:
            return self.queryset.filter(project__id=pk)

        elif is_project  == 0:
            return self.queryset.filter(sites__id=pk)


class StepsViewSet(viewsets.ModelViewSet):

    serializer_class = StepsSerializer
    queryset = Step.objects.all()


