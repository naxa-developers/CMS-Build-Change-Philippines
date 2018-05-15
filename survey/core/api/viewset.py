from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, mixins
from core.models import Project, Step
from .serializers import ProjectSerializer, StepsSerializer
from core.api.serializers import StepSerializer, ChecklistSerializer
from core.models import Checklist, Step, Project

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


class StepViewset(viewsets.ModelViewSet):
    serializer_class = StepSerializer
    queryset = Step.objects.all()
    
    def get_queryset(self):
        site = self.kwargs.get('site', False)
        if site:
            self.queryset = self.queryset.filter(site__id=site)
        return self.queryset


    def perform_create(self, serializer, **kwargs):
        localname = serializer.initial_data.get('localname', '')
        data = serializer.save(localname=localname)
        return data


class ChecklistViewset(viewsets.ModelViewSet):
    serializer_class = ChecklistSerializer
    queryset = Checklist.objects.all()
    
    def get_queryset(self):
        step = self.kwargs.get('step', False)
        if step:
            self.queryset = self.queryset.filter(step__id=step)
        return self.queryset

    def perform_create(self, serializer, **kwargs):
        localtext = serializer.initial_data.get('localtext', '')
        data = serializer.save(localtext=localtext)
        return data

