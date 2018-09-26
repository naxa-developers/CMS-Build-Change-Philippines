from django.contrib.auth.models import User, Group

from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response

from userrole.models import UserRole

from core.api.serializers import StepSerializer, ChecklistSerializer
from core.models import Checklist, Step, Project, Material, Report, Category, SiteMaterials, SiteDocument, SiteSteps, ConstructionSteps, SubStepCheckList
from .serializers import ProjectSerializer, StepsSerializer, MaterialSerializer, ReportSerializer, CategorySerializer,\
    SiteMaterialSerializer, SiteDocumentSerializer, SiteReportSerializer, SiteEngineerSerializer, SubStepsCheckListSerializer

# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'email')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        UserRole.objects.create(user=user, group=Group.objects.get(name='Community Member'), project_id=1)
        return user


@permission_classes((AllowAny, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


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
    serializer_class = SubStepsCheckListSerializer
    queryset = SubStepCheckList.objects.all()
    
    def get_queryset(self):
        step = self.kwargs.get('step', False)
        if step:
            self.queryset = self.queryset.filter(step__id=step)
        return self.queryset

    # def perform_create(self, serializer, **kwargs):
    #     localtext = serializer.initial_data.get('localtext', '')
    #     data = serializer.save(localtext=localtext)
    #     return data


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
    queryset = UserRole.objects.filter(group__name="Field Engineer")

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


@api_view(['GET'])
def construction_site_steps_update(request):
    value = request.GET.get('value', None)
    checkbox_value = request.GET.get('checkbox_value', None)
    site_id = request.GET.get('site_id', None)

    if checkbox_value is '1':

        SiteSteps.objects.get_or_create(site_id=site_id, step=ConstructionSteps.objects.get(name=value))
    else:
        SiteSteps.objects.filter(site_id=site_id, step=ConstructionSteps.objects.get(name=value)).delete()

    data = {
        'success': 'hello',

    }

    return Response(data)
