from django.contrib.auth.models import User, Group

from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from userrole.models import UserRole

from core.api.serializers import StepSerializer, ChecklistSerializer
from core.models import Checklist, Step, Project, Material, Report, Category, SiteMaterials, SiteDocument
from .serializers import ProjectSerializer, StepsSerializer, MaterialSerializer, ReportSerializer, CategorySerializer,\
    SiteMaterialSerializer, SiteDocumentSerializer, SiteReportSerializer, SiteEngineerSerializer

# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'email')

        write_only_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


@permission_classes((AllowAny, ))
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


class MaterialViewset(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()

    def get_queryset(self):
        project = self.kwargs.get('project', False)
        if project:
            self.queryset = self.queryset.filter(project__id=project)
        return self.queryset

    def perform_create(self, serializer, **kwargs):
        data = serializer.save(created_by=self.request.user)
        return data


class ReportViewset(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related()

    def perform_create(self, serializer, **kwargs):
        localname = serializer.initial_data.get('localname', '')
        data = serializer.save(localname=localname)
        return data


class SiteMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteMaterialSerializer
    queryset = SiteMaterials.objects.all()

    def get_queryset(self):
        site = self.kwargs.get('site', False)
        if site:
            self.queryset = self.queryset.filter(site=site)
        return self.queryset


class SiteReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteReportSerializer
    queryset = Report.objects.all()

    def get_queryset(self):
        site = self.kwargs.get('site', False)
        if site:
            self.queryset = self.queryset.filter(checklist__step__site=site)
        return self.queryset


class SiteEngineerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteEngineerSerializer
    queryset = UserRole.objects.all()

    def get_queryset(self):
        site = self.kwargs.get('site', False)
        if site:
            self.queryset = self.queryset.filter(site__id=site)
        return self.queryset


class SiteDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteDocumentSerializer
    queryset = SiteDocument.objects.all()

    def get_queryset(self):
        site = self.kwargs.get('site', False)
        if site:
            self.queryset = self.queryset.filter(site=site)
        return self.queryset