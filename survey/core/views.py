import os
import zipfile
from itertools import chain
import csv
import xlwt
import io
import reportlab
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

from django.http import FileResponse
from reportlab.pdfgen import canvas

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.utils import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.files.storage import FileSystemStorage

from django.conf import settings
from survey.settings import BASE_DIR
from userrole.forms import UserProfileForm
from userrole.models import UserRole
from .models import Project, Site, Category, Material, Step, Report, ReportFeedback, SiteMaterials, SiteDocument, Checklist, ConstructionSteps, \
    ConstructionSubSteps, CONSTRUCTION_STEPS_LIST, CONSTRUCTION_SUB_STEPS_LIST, SiteSteps, SubStepCheckList, SubstepReport, \
    Notification, HousesAndGeneralConstructionMaterials, BuildAHouseMakesHouseStrong, BuildAHouseKeyPartsOfHouse, \
    StandardSchoolDesignPDF, CallLog, EventLog, NewCommonSubStepChecklist, NewSubStepChecklist, SiteReport
from .forms import ProjectForm, CategoryForm, MaterialForm, SiteForm, SiteMaterialsForm, SiteDocumentForm, \
    UserCreateForm, SiteConstructionStepsForm, ConstructionSubStepsForm, PrimaryPhotoFormset, \
     BadPhotoFormset, GoodPhotoFormset, NewCommonChecklistForm, NewChecklistFormset, ConstructionSubStepsChoiceForm, \
    HousesAndGeneralConstructionMaterialsForm, BuildAHouseMakesHouseStrongForm, BuildAHouseKeyPartsOfHouseForm, \
    SubstepReportForm, ReportFeedbackForm
from .rolemixins import ProjectRoleMixin, SiteRoleMixin, CategoryRoleMixin, ProjectGuidelineRoleMixin, \
    SiteGuidelineRoleMixin, DocumentRoleMixin, ReportRoleMixin
from django.core import serializers
from .admin import SubStepCheckListResource
from django.forms.models import inlineformset_factory
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from fcm_django.models import FCMDevice
from django.db import transaction


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def token(request):

    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            project_id, role = user.user_roles.values_list('project_id', 'group__name')[0]
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'project': project_id,
                'group': role
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                 'error': 'Bad password',
                 'msg': 'Invalid Password',
                'data': request.POST
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'error': str(e),
            'msg': 'Invalid Username and Password',
            'data': request.POST
        }, status=status.HTTP_400_BAD_REQUEST)


def project_material_photos(request, project_id):

    # response = HttpResponse(content_type='application/zip')
    # zip_file = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)
    zip_file = zipfile.ZipFile(os.path.join(BASE_DIR) + '/media/ProjectMaterialPhotos.zip', 'w', zipfile.ZIP_DEFLATED)

    material_photos = ConstructionSubSteps.objects.filter(project_id=project_id)
    project = get_object_or_404(Project, id=project_id)
    category_materials = Material.objects.filter(project_id=project_id)
    step_image = ConstructionSteps.objects.filter(project_id=project_id)
    more_about_materials = HousesAndGeneralConstructionMaterials.objects.all()
    my_house_strong = BuildAHouseMakesHouseStrong.objects.all()
    key_parts_of_house = BuildAHouseKeyPartsOfHouse.objects.all()
    standard_school_design_pdf = StandardSchoolDesignPDF.objects.all()
    site_docs = SiteDocument.objects.all()

    for site_doc in site_docs:
        if site_doc.file:
            zip_file.write(os.path.join(BASE_DIR) + site_doc.file.url, arcname=site_doc.file.url)


    for filename in category_materials:
        if filename.good_photo:
            zip_file.write(os.path.join(BASE_DIR) + filename.good_photo.url, arcname=filename.good_photo.url)
        if filename.bad_photo:
            zip_file.write(os.path.join(BASE_DIR) + filename.bad_photo.url, arcname=filename.bad_photo.url)


    for filename in material_photos:
        if filename.good_photos:
            for file in filename.good_photos.all():
                if 'media/' + str(file.image) in [i.filename for i in zip_file.infolist()]:
                    print('YESSSSSSSSSSSS', file.image)
                else:
                    zip_file.write(os.path.join(BASE_DIR) + '/media/' + str(file.image),
                                   arcname='/media/' + str(file.image))
                # zip_file.write(os.path.join(BASE_DIR) + '/media/'+str(file.image), arcname='/media/'+str(file.image))
        if filename.bad_photos:
            for file in filename.bad_photos.all():
                if 'media/' + str(file.image) in [i.filename for i in zip_file.infolist()]:
                    print('YESSSSSSSSSSSS', file.image)
                else:
                    zip_file.write(os.path.join(BASE_DIR) + '/media/' + str(file.image),
                                   arcname='/media/' + str(file.image))
                # zip_file.write(os.path.join(BASE_DIR) + '/media/'+str(file.image), arcname='/media/'+str(file.image))

        if filename.primary_photos:
            for file in filename.primary_photos.all():
                if 'media/' + str(file.image) in [i.filename for i in zip_file.infolist()]:
                    print('YESSSSSSSSSSSS', file.image)
                else:
                    zip_file.write(os.path.join(BASE_DIR) + '/media/' + str(file.image),
                                   arcname='/media/' + str(file.image))
    for img in step_image:
        if img.image:

            zip_file.write(os.path.join(BASE_DIR) + img.image.url, arcname=img.image.url)
        if img.icon:
            if 'media/' + str(img.icon) in [i.filename for i in zip_file.infolist()]:
                print('YESSSSSSSSSSSS', img.icon)
            else:
                zip_file.write(os.path.join(BASE_DIR) + img.icon.url, arcname=img.icon.url)

    for img in more_about_materials:
        if img.good_photo:
            zip_file.write(os.path.join(BASE_DIR) + img.good_photo.url, arcname=img.good_photo.url)

        if img.bad_photo:
            zip_file.write(os.path.join(BASE_DIR) + img.bad_photo.url, arcname=img.bad_photo.url)

    for img in key_parts_of_house:
        if img.good_photo:
            zip_file.write(os.path.join(BASE_DIR) + img.good_photo.url, arcname=img.good_photo.url)

        if img.bad_photo:
            zip_file.write(os.path.join(BASE_DIR) + img.bad_photo.url, arcname=img.bad_photo.url)

    for data in my_house_strong:
        if data.pdf:
            zip_file.write(os.path.join(BASE_DIR) + data.pdf.url, arcname=data.pdf.url)

    for data in standard_school_design_pdf:
        if data.pdf:
            zip_file.write(os.path.join(BASE_DIR) + data.pdf.url, arcname=data.pdf.url)


    # response['Content-Disposition'] = 'attachment; filename={}MaterialPhotos.zip'.format(project.name)
    messages.success(request, 'successfully created zip')
    return HttpResponseRedirect(reverse('core:project_dashboard', args=[project_id]))



def site_documents_zip(request, site_id):

    response = HttpResponse(content_type='application/zip')
    zip_file = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)
    site_documents = SiteDocument.objects.filter(site=site_id)
    site = get_object_or_404(Site, id=site_id)

    for filename in site_documents:
        if filename.file:
            zip_file.write(os.path.join(BASE_DIR) + filename.file.url, arcname=filename.file.url)

    response['Content-Disposition'] = 'attachment; filename={}Documents.zip'.format(site.name)
    return response

# def site_documents_zip(request, site_id):
#
#     # response = HttpResponse(content_type='application/zip')
#     zip_file = zipfile.ZipFile(os.path.join(BASE_DIR)+'/abc.zip', 'w', zipfile.ZIP_DEFLATED)
#     site_documents = SiteDocument.objects.filter(site=site_id)
#     site = get_object_or_404(Site, id=site_id)
#
#     for filename in site_documents:
#         if filename.file:
#             zip_file.write(os.path.join(BASE_DIR) + filename.file.url, arcname=filename.file.url)
#
#     # response['Content-Disposition'] = 'attachment; filename={}Documents.zip'.format(site.name)
#     return HttpResponse('successs')


class ProjectPersonnelList(TemplateView):
    """
    List of Project Manage and Field Engineers
    """
    template_name = 'core/project_personnel_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']
        context['project'] = get_object_or_404(Project, id=project_id)
        context['project_personnel_list'] = UserRole.objects.filter(Q(group__name='Field Engineer') |
                                                                    Q(group__name='Project Manager') |
                                                                    Q(group__name='Community Member'),
                                                                    project_id=project_id)

        return context


class CommunityUsersList(TemplateView):
    template_name = 'core/community_users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']
        context['project'] = get_object_or_404(Project, id=project_id)
        context['community_users_list'] = UserRole.objects.filter(Q(group__name='Community Member'), project_id=project_id)
        return context


class SuperAdminMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.group.name == "Super Admin":
                return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied


class ManagerSuperAdminMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.group.name == "Super Admin" or request.group.name == "Project Manager":
                return super(ManagerSuperAdminMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm
    context_object_name = 'projects'

    def get_success_url(self):
        if self.request.group.name == "Project Manager":
            project_id = Project.objects.get(project_roles__user=self.request.user).pk
            return reverse('core:project_dashboard', kwargs={'project_id': project_id})
        elif self.request.group.name == "Super Admin":
            return reverse('core:admin_dashboard')


class ProjectCreateView(SuperAdminMixin, ProjectMixin, CreateView):
    """
    Project CreateView
    """
    template_name = "core/project_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.group.name == "Super Admin":
            context['projects'] = Project.objects.all()
            return context
        elif self.request.group.name == "Project Manager":
            context['project'] = Project.objects.get(project_roles__user=self.request.user)
            return context

    def form_valid(self, form):
        self.object = form.save()
        project_id = self.object.id
        for step in CONSTRUCTION_STEPS_LIST:
            ConstructionSteps.objects.create(name=step, project_id=project_id)

        # for step_substeps in CONSTRUCTION_SUB_STEPS_LIST:
        #     for step in step_substeps.keys():
        #         for substeps_list in step_substeps.values():
        #             for substep in substeps_list:
        #                 ConstructionSubSteps.objects.get_or_create(title=substep, step=ConstructionSteps.objects.get(name=step), created_by=self.request.user)

        return super().form_valid(form)


class ProjectDetailView(SuperAdminMixin, ProjectMixin, DetailView):
    """
    Project DetailView
    """
    template_name = "core/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        context['materials_list'] = Project.objects.filter(pk=self.kwargs['pk'])\
                                .prefetch_related('material')\
                                .values_list('material__id','material__title', 'material__category',\
                                             'material__category__name',\
                                             'material__good_photo', 'material__bad_photo')
        context['if_material'] = Material.objects.filter(project=self.kwargs['pk']).count()
        context['category_list'] = Project.objects.filter(pk=self.kwargs['pk'])\
                                .prefetch_related('category')\
                                .values_list('category', 'category__name')
        context['if_category'] = Category.objects.filter(project=self.kwargs['pk']).count()
        return context


class ProjectUpdateView(ProjectMixin, ProjectRoleMixin, UpdateView):
    """
    Project UpdateView
    """
    template_name = "core/project_form.html"
    model = Project
    context_object_name = 'project'


class ProjectDeleteView(SuperAdminMixin, ProjectMixin, DeleteView):
    """
    Project DeleteView
    """
    template_name = "core/project_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.group.name == "Super Admin":
            context['projects'] = Project.objects.all()
            return context
        elif self.request.group.name == "Project Manager":
            context['project'] = Project.objects.get(project_roles__user=self.request.user)
            return context


class UserCreateView(SuperAdminMixin, CreateView):
    """
    User SignUp form
    """
    form_class = UserProfileForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['users'] = User.objects.all()
        return context

    def get_success_url(self):
        return reverse('core:admin_dashboard')


class UserListView(SuperAdminMixin, ListView):
    model = User
    template_name = 'registration/user_list.html'
    context_object_name = "users"


class ProjectDashboard(ProjectRoleMixin, TemplateView):
    """
    dashboard for Project Manager
    """

    template_name = "core/project_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['materials_list'] = Material.objects.filter(project=self.kwargs['project_id'])
        context['users'] = User.objects.filter(user_roles__project__id=self.kwargs['project_id'],\
                                               user_roles__group__name__exact="Project Manager")
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_id'])
        # context['category_list'] = Category.objects.filter(project=self.kwargs['project_id'])
        context['construction_steps_list'] = ConstructionSteps.objects.filter(project_id=self.kwargs['project_id']).order_by('order')
        context['total_reports'] = Report.objects.filter(checklist__step__site__project__id=self.kwargs['project_id']).count()
        context['assigned_manager'] = User.objects.filter(user_roles__project=self.kwargs['project_id']).first()
        context['project_managers'] = UserRole.objects.filter(project_id=self.kwargs['project_id'], group__name="Project Manager").values('user__username', 'pk')


        project_id=self.kwargs['project_id']

        # Count Total images for zip file comparison
        good_material_photos=0
        bad_material_photos=0
        primary_material_photos=0
        material_photos=ConstructionSubSteps.objects.filter(project_id=project_id)
        for filename in material_photos:
            if filename.good_photos.all():
                good_material_photos=good_material_photos+1
            if filename.bad_photos.all():
                bad_material_photos=bad_material_photos+1
            if filename.primary_photos.all():
                primary_material_photos=primary_material_photos+1

        good_category_materials = Material.objects.filter(project_id=project_id).exclude(good_photo__exact='').count()
        bad_category_materials = Material.objects.filter(project_id=project_id).exclude(bad_photo__exact='').count()

        step_image = ConstructionSteps.objects.filter(project_id=project_id).exclude(image__exact='').count()
        icon_image = ConstructionSteps.objects.filter(project_id=project_id).exclude(icon__exact='').count()

        good_more_about_materials = HousesAndGeneralConstructionMaterials.objects.all().exclude(good_photo__exact='').count()
        bad_more_about_materials = HousesAndGeneralConstructionMaterials.objects.all().exclude(bad_photo__exact='').count()

        my_house_strong = BuildAHouseMakesHouseStrong.objects.all().exclude(pdf__exact='').count()

        good_key_parts_of_house = BuildAHouseKeyPartsOfHouse.objects.all().exclude(good_photo__exact='').count()
        bad_key_parts_of_house = BuildAHouseKeyPartsOfHouse.objects.all().exclude(bad_photo__exact='').count()

        standard_school_design_pdf = StandardSchoolDesignPDF.objects.all().exclude(pdf__exact='').count()
        site_docs = SiteDocument.objects.all().exclude(file__exact='').count()

        total_images = good_material_photos+bad_material_photos+primary_material_photos+good_category_materials+bad_category_materials\
        +step_image+icon_image+good_more_about_materials+bad_more_about_materials+my_house_strong+good_key_parts_of_house\
        +bad_key_parts_of_house+standard_school_design_pdf+site_docs
        # print('Totalllll', total_images)

        try:
            DIR=os.path.join(BASE_DIR) + '/media/ProjectMaterialPhotos.zip'
            zfile = zipfile.ZipFile(DIR, 'r')
            total_zip_images=0
            for finfo in zfile.infolist():
                if isinstance(finfo, zipfile.ZipInfo):
                    total_zip_images=total_zip_images+1
            # print('zip ko imagessss',total_zip_images)
            if total_images > total_zip_images or total_images < total_zip_images:
                context['create_zip'] = True
        except:
            pass

        site_geojson = Site.objects.filter(\
            project__id=self.kwargs['project_id']).exclude(location__isnull=True)
        if site_geojson.exists():
            context['locations'] = serializers.serialize('geojson', site_geojson, fields=('location', 'name', 'address', 'pk'))
        else:
            context['locations'] = [[]]
        site_address = Site.objects.exclude(location__isnull=True).filter(project__id=self.kwargs['project_id']).values_list('address', flat=True)
        json_site_address = json.dumps(list(site_address))
        context['site_address'] = json_site_address
        site_latlong_object = Site.objects.exclude(location__isnull=True).filter(project__id=self.kwargs['project_id']).values_list('location', flat=True)
        context['site_latlong'] = json.dumps([[l.x, l.y] for l in site_latlong_object])
        context['recent_activities_report'] = SubstepReport.objects.filter(site__project_id=self.kwargs['project_id']).order_by('date')[:5]
        context['recent_activities_site_report'] = SiteReport.objects.filter(site__project_id=self.kwargs['project_id']).order_by('date')[:5]
        context['call_logs'] = CallLog.objects.all().select_related('call_to', 'call_from').order_by('-pk')
        # context['event_logs'] = EventLog.objects.all().order_by('-date')

        if self.request.group.name == "Super Admin":
            context['projects'] = Project.objects.all()
            return context
        return context


class RecentUpdates(ProjectRoleMixin, TemplateView):
    """
    Recent Updates
    """

    template_name = "core/recent_updates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, id=self.kwargs['project_id'])
        context['recent_activities_report'] = SubstepReport.objects.filter(site__project_id=self.kwargs['project_id']).order_by('-date')
        # context['event_logs'] = EventLog.objects.all().order_by('-date')

        return context


class Dashboard(SuperAdminMixin, TemplateView):
    """
    dashboard for Super Admin
    """
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['total_projects'] = Project.objects.all().count()
        context['users'] = User.objects.all()[:20]
        context['total_project_managers'] = User.objects.filter(user_roles__group__name='Project Manager').count()
        return context


class SiteCreateView(SiteRoleMixin, CreateView):
    """
    Site Create Form
    """

    template_name = "core/site_create.html"
    model = Site
    form_class = SiteForm

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        return context

    def get_success_url(self):
        if self.request.group.name == "Super Admin":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url

        elif self.request.group.name == "Project Manager":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url


class SiteListView(ManagerSuperAdminMixin, ListView):
    """
    Site List View
    """

    template_name = "core/site_list.html"
    model = Site
    paginate_by = 100


class SiteDetailView(SiteRoleMixin, DetailView):
    """
    Site Detail View
    """
    template_name = "core/site_detail.html"
    model = Site
    context_object_name = 'site'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step_list'] = Step.objects.filter(site=self.kwargs['pk'])[:10]
        context['site_materials'] = SiteMaterials.objects.filter(site=self.kwargs['pk'])[:5]
        substep_report = SubstepReport.objects.filter(site_id=self.kwargs['pk'])[:10]
        site_report = SiteReport.objects.filter(site_id=self.kwargs['pk'])[:5]
        result_list = sorted(
            chain(substep_report, site_report),
            key=lambda instance: instance.date, reverse=True)
        context['reports'] = result_list
        context['project'] = Project.objects.get(sites=self.kwargs['pk'])
        context['site_engineers'] = UserRole.objects.filter(site__id=self.kwargs['pk'], group__name='Field Engineer')\
                                    .values_list('user__username','id')
        context['site_documents'] = SiteDocument.objects.filter(site__id=self.kwargs['pk'])[:6]
        context['site_pictures'] = SubstepReport.objects.filter(site_id=self.kwargs['pk'])[:10]
        context['construction_steps_list'] = SiteSteps.objects.filter(site_id=self.kwargs['pk']).order_by('step__order')
        checklist_status_true_count = Checklist.objects.filter(step__site__id=self.kwargs['pk'], status=True).count()
        total_site_checklist_count = Checklist.objects.filter(step__site__id=self.kwargs['pk']).count()
        if total_site_checklist_count:
            context['progress'] = round((checklist_status_true_count/total_site_checklist_count)*100)
        else:
            context['progress'] = 0
        return context


class PictureList(TemplateView):
    template_name = 'core/picture_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_pictures'] = SubstepReport.objects.all().values_list('photo')
        return context



class SiteDetailTemplateView(TemplateView):

    template_name = 'core/site_detail_js.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(sites=self.kwargs['site_pk'])
        context['site_id'] = self.kwargs['site_pk']
        context['site'] = serializers.serialize('json', [Site.objects.get(id=self.kwargs['site_pk'])], ensure_ascii=False)[1:-1]
        context['document_url'] = reverse('core:document_list',  kwargs={'site_id': self.kwargs['site_pk']})
        context['add_user_url'] = reverse('userrole:project_user_create',  kwargs={'project_id': project.id})
        context['people_url'] = reverse('userrole:field_engineer_create',  kwargs={'site_id': self.kwargs['site_pk']})
        context['site_edit_url'] = reverse('core:site_update',  kwargs={'pk': self.kwargs['site_pk']})
        context['site_delete_url'] = reverse('core:site_delete',  kwargs={'pk': self.kwargs['site_pk']})

        return context


class SiteUpdateView(SiteRoleMixin, UpdateView):
    """
    Site Update View
    """
    template_name = "core/site_create.html"
    model = Site
    form_class = SiteForm

    def form_valid(self, form):
        form.instance.site = get_object_or_404(Site, pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(sites=self.kwargs['pk'])
        return context

    def get_success_url(self):
        if self.request.group.name == "Super Admin":
            success_url = reverse_lazy('core:site_detail', args=(self.object.pk,))
            return success_url

        elif self.request.group.name == "Project Manager":
            success_url = reverse_lazy('core:site_detail', args=(self.object.pk,))
            return success_url


class SiteDeleteView(SiteRoleMixin, DeleteView):
    """
    Site Delete View
    """
    model = Site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(sites=self.kwargs['pk'])

        return context

    def get_success_url(self):
        if self.request.group.name == "Super Admin":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url

        elif self.request.group.name == "Project Manager":
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class SiteStepsView(ManagerSuperAdminMixin, TemplateView):
    """
    Site Steps View
    """
    template_name = "core/site_steps.html"
    # template_name = "_base.html"
    # template_name = "_dashboard.html"

    def get_context_data(self, **kwargs):
        data = super(SiteStepsView, self).get_context_data(**kwargs)
        if data['is_project'] == 0:
            project = Site.objects.get(pk=data['pk']).project.id
            data['project'] = project
            data['site'] = Site.objects.select_related().get(id=self.kwargs['pk'])
            if self.request.user.is_superuser:
                data['dashboard_url'] = reverse('core:admin_dashboard')
            else:
                data['dashboard_url'] = reverse('core:project_dashboard',  kwargs={'project_id': project})
        else:
            data['project'] = data['pk']
            if self.request.user.is_superuser:
                data['dashboard_url'] = reverse('core:admin_dashboard')
            else:
                data['dashboard_url'] = reverse('core:project_dashboard',  kwargs={'project_id': data['pk']})
        return data


class CategoryFormView(CategoryRoleMixin, FormView):
    """
    Category Form View
    """
    template_name = "core/category_create.html"
    form_class = CategoryForm
    model = Category

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])

        return context

    def get_success_url(self):
            success_url = reverse_lazy('core:category_list', args=(self.kwargs['project_id'],))
            return success_url


class CategoryListView(CategoryRoleMixin, ListView):
    """
    Category ListView
    """
    template_name = "core/category_list.html"
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        context['category_list'] = Category.objects.filter(project=self.kwargs['project_id'])

        return context

class CategoryDetailView(DetailView):
    model = Category
    temlate_name = "core/category_detail.html"


class CategoryUpdateView(CategoryRoleMixin, UpdateView):
    """
    Category UpdateView
    """
    template_name = "core/category_create.html"
    form_class = CategoryForm
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.get(project_roles__user=self.request.user)
            # context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
            success_url = reverse_lazy('core:category_list', args=(self.object.project.pk,))
            return success_url


class CategoryDeleteView(CategoryRoleMixin, DeleteView):
    """
    Category DeleteView
    """
    model = Category
    template_name = "core/category_confirm_delete.html"

    def get_success_url(self):
            success_url = reverse_lazy('core:category_list', args=(self.object.project.pk,))
            return success_url


class CategoryMaterialView(TemplateView):
    template_name = 'core/category_material.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(category=self.kwargs['category_pk'])
        context['category'] = Category.objects.get(id=self.kwargs['category_pk'])
        context['category_material'] = Material.objects.filter(category_id=self.kwargs['category_pk'])
        return context


class MaterialFormView(ProjectGuidelineRoleMixin, FormView):
    """
    Material From View
    """
    template_name = "core/material_form.html"
    form_class = MaterialForm

    # def get_form(self, form_class=None):
    #     form = super(MaterialFormView, self).get_form(form_class=self.form_class)
    #     form.fields['category'].queryset = form.fields['category'].queryset.filter(project=self.kwargs['project_id'])
    #     return form

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.instance.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        return context

    def get_success_url(self):
            success_url = reverse_lazy('core:material_list', args=(self.kwargs['project_id'],))
            return success_url


class MaterialUpdateView(ProjectGuidelineRoleMixin, UpdateView):
    """
    Category UpdateView
    """
    template_name = "core/material_form.html"
    form_class = MaterialForm
    model = Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.get(project_roles__user=self.request.user)
            # context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.group.name == "Super Admin":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url
        elif self.request.group.name == "Project Manager":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url


class MaterialDeleteView(ProjectGuidelineRoleMixin, DeleteView):
    """
    Category DeleteView
    """
    model = Material
    template_name = "core/material_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(material=self.kwargs['pk'])
        return context

    def get_success_url(self):
        if self.request.group.name == "Super Admin":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url

        elif self.request.group.name == "Project Manager":
            success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
            return success_url


class MaterialDetailView(ProjectGuidelineRoleMixin, DetailView):
    """
    Category UpdateView
    """
    template_name = "core/material_detail.html"
    model = Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(material=self.kwargs['pk'])

        return context


class MaterialListView(ManagerSuperAdminMixin, ListView):
    """
    Category UpdateView
    """
    template_name = "core/material_list.html"
    model = Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            context['project'] = Project.objects.get(pk=self.kwargs['pk'])
            context['materials_list'] = Material.objects.filter(project=self.kwargs['pk'])
            context['if_material'] = Material.objects.filter(project=self.kwargs['pk']).count()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.get(project_roles__user=self.request.user)
            context['materials_list'] = Material.objects.filter(project__project_roles__user=self.request.user)
            context['project_id'] = self.kwargs['pk']
            return context

        else:
            raise PermissionDenied


class SiteMaterialFormView(SiteGuidelineRoleMixin, CreateView):
    model = SiteMaterials
    form_class = SiteMaterialsForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['materials'].queryset = form.fields['materials'].queryset.filter(project__sites=self.kwargs['site_id'])\
                                            .distinct()
        return form

    def form_valid(self, form):
        form.instance.site = get_object_or_404(Site, pk=self.kwargs['site_id'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse_lazy('core:site_detail', args=(self.object.site.pk,))
        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(sites=self.kwargs['site_id'])
        return context


class SiteMaterialListView(SiteGuidelineRoleMixin, ListView):
    model = SiteMaterials
    form_class = SiteMaterialsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_materials'] = SiteMaterials.objects.filter(site=self.kwargs['site_id'])
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])

        return context


class SiteMaterialDetailView(SiteGuidelineRoleMixin, DetailView):
    model = SiteMaterials
    form_class = SiteMaterialsForm
    context_object_name = 'site_material'


class SiteMaterialDeleteView(SiteGuidelineRoleMixin, DeleteView):
    model = SiteMaterials
    form_class = SiteMaterialsForm

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        materials = self.object.materials.all()
        site = Site.objects.get(site_site_materials=self.model.pk)
        sitematerials = SiteMaterials.objects.filter(site=site)
        sitematerials_list=[]
        [sitematerials_list.append(sm.materials.all()) for sm in sitematerials]
        success_url = reverse_lazy('core:site_material_list', args=(self.object.site.pk,))
        self.object.materials.remove(materials)
        return HttpResponseRedirect(success_url)


def ExportReport(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('SubstepReport')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # columns = ['User', 'Comment', 'Site', 'Status', 'Feedback']
    columns = ['Date', 'User', 'School', 'Step', 'Substep', 'User Report', 'Reply']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # substep_report = SubstepReport.objects.all().values_list('user__username', 'comment', 'site', 'status', 'feedback__feedback')
    # site_report = SiteReport.objects.all().values_list('user__username', 'comment', 'site', 'status', 'feedback__feedback')
   
    substep_report = SubstepReport.objects.all().values_list('date', 'user__username', 'site__name', 'step__step__name', 'substep__title', 'comment', 'feedback__feedback')

    # rows = list(chain(substep_report, site_report))

    rows = list(substep_report)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def ExportPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="download.pdf"'

    p = canvas.Canvas(response)
    query_set = SubstepReport.objects.all()
    count = 0
    for qs in query_set:
        y = 900 - count * 100
        p.drawString(0, y+30, "Date: " + str(qs.date))
        p.drawString(0, y+20, "User: " + qs.user.username)
        p.drawString(0, y+10, "School: " + qs.site.name)
        p.drawString(0, y, "Step: " + qs.step.step.name)
        p.drawString(0, y-10, "Substep: " + qs.substep.title)
        p.drawString(0, y-20, "User Report: " + qs.comment)
        p.drawString(0, y-30, "Reply: " + str(qs.feedback))
        # p.drawString(0, y-40, "Photo: " + str(qs.photo))
        count = count + 1

    p.showPage()
    p.save()
    return response


class SubstepReportListView(ReportRoleMixin, ListView):
    """
    Report List
    """
    model = SubstepReport
    template_name = "core/substepreport_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # substep_report = SubstepReport.objects.filter(site_id=self.kwargs['pk'])[:10]
        # site_report = SiteReport.objects.filter(site_id=self.kwargs['pk'])[:5]
        # result_list = sorted(
        #     chain(substep_report, site_report),
        #     key=lambda instance: instance.date, reverse=True)
        # context['reports'] = result_list

        substep_report = SubstepReport.objects.filter(category=0)
        site_report = SiteReport.objects.filter(site_id=self.kwargs['pk'])[:5]
        result_list = sorted(
            chain(substep_report, site_report),
            key=lambda instance: instance.date, reverse=True)
        context['reports'] = result_list

        substep_report1 = SubstepReport.objects.filter(category=1)
        site_report1 = SiteReport.objects.filter(site_id=self.kwargs['pk'])[:5]
        result_list1 = sorted(
            chain(substep_report1, site_report1),
            key=lambda instance: instance.date, reverse=True)
        context['report1'] = result_list1


        substep_report2 = SubstepReport.objects.filter(category=2)
        site_report2 = SiteReport.objects.filter(site_id=self.kwargs['pk'])[:5]
        result_list2 = sorted(
            chain(substep_report2, site_report2),
            key=lambda instance: instance.date, reverse=True)
        context['report2'] = result_list2

        context['site'] = Site.objects.get(id=self.kwargs['pk'])
        context['project'] = Project.objects.get(sites=self.kwargs['pk'])
        return context


class SubstepReportDetailView(ReportRoleMixin, DetailView):
    """
    Report detail
    """
    model = SubstepReport
    template_name = 'core/substepreport_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = SubstepReport.objects.filter(id=self.kwargs['pk'])
        context['site'] = Site.objects.get(id=self.object.site.id)
        context['project'] = Project.objects.get(sites=self.object.site.id)
        context['choices'] = SubstepReport._meta.get_field('status').choices
        return context
    
    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        if request.POST.get('status'):
            sub_step = SubstepReport.objects.get(id=self.kwargs['pk'])
            sub_step.status=request.POST.get('status')
            sub_step.save()
            return HttpResponseRedirect('/core/substep-report-detail/%s' %self.kwargs['pk'])

        with transaction.atomic():
            try:
                if request.POST.get('feedback_submit'):
                    report_feedback = ReportFeedback()
                    report_feedback.user = self.request.user
                    report_feedback.feedback = request.POST.get('feedback_text')
                    report_feedback.save()

                    subreport = SubstepReport.objects.get(id=self.kwargs['pk'])
                    subreport.feedback = report_feedback
                    subreport.save()

                    message_title = "User " + self.request.user.username + " Sent Feedback " + report_feedback.feedback
                    message_body = subreport.site.name + " - " + subreport.step.step.name + " - " + subreport.substep.title

                    try:
                        subreport = SubstepReport.objects.get(id=self.kwargs['pk'])
                        report_data = {
                            'report_id':subreport.id,
                            'user': subreport.user.username,
                            'status': subreport.status,
                            'site': subreport.site.name,
                            'step':subreport.step.step.name,
                            'substep':subreport.substep.title,
                            'comment':subreport.comment, 
                            'feedback':request.POST.get('feedback_text')
                            }
                        message = subreport.site.name + " - " + subreport.step.step.name + "-" + subreport.substep.title
                        FCMDevice.objects.filter(user=User.objects.get(id=SubstepReport.objects.get(id=self.kwargs.get('pk')).user_id)).send_message(title=message_title, body=message_body, data={'report_data': report_data, 'message': message})
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e) 
        return HttpResponseRedirect('/core/substep-report-detail/%s' %self.kwargs['pk'])


class SiteReportDetailView(ReportRoleMixin, DetailView):
    """
    Site Report Detail
    """
    model = SiteReport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = SiteReport.objects.filter(id=self.kwargs['pk'])
        context['site'] = Site.objects.get(id=self.object.site.id)
        context['project'] = Project.objects.get(sites=self.object.site.id)
        context['choices'] = SiteReport._meta.get_field('status').choices
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('status'):
            sitereport = SiteReport.objects.get(id=self.kwargs['pk'])
            sitereport.status=request.POST.get('status')
            sitereport.save()
            return HttpResponseRedirect('/core/site-report-detail/%s' %self.kwargs['pk'])
        
        with transaction.atomic():
            try:
                if request.POST.get('feedback_submit'):
                    report_feedback = ReportFeedback()
                    report_feedback.user = self.request.user
                    report_feedback.feedback = request.POST.get('feedback_text')
                    report_feedback.save()

                    sitereport = SiteReport.objects.get(id=self.kwargs['pk'])
                    sitereport.feedback = report_feedback
                    sitereport.save()

                    message_title = "User " + self.request.user.username + " Sent Feedback " + report_feedback.feedback
                    message_body = sitereport.site.name

                    try:
                        report_data = {
                            'report_id':sitereport.id,
                            'user': sitereport.user.username,
                            'status': sitereport.status,
                            'site': sitereport.site.name,
                            'comment':sitereport.comment, 
                            'feedback':request.POST.get('feedback_text')
                            }
                        message = sitereport.site.name
                        FCMDevice.objects.filter(user=User.objects.get(id=SiteReport.objects.get(id=self.kwargs.get('pk')).user_id)).send_message(title=message_title, body=message_body, data={'report_data': report_data, 'message': message})
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
        return HttpResponseRedirect('/core/site-report-detail/%s' %self.kwargs['pk'])

            


class SiteReportDeleteView(DeleteView):
    model = SiteReport
    template_name = "core/sitereport_delete.html"

    def get_success_url(self):
        site_id = Site.objects.get(site_reports=self.kwargs['pk']).id
        success_url = reverse_lazy('core:site_report_list', args=[site_id],)
        return success_url

# class PhotoDelete(TemplateView):
#     template_name = "core/substepreport_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['substepreport'] = SubstepReport.objects.



class SiteReportListView(ReportRoleMixin, ListView):
    """
    Report List
    """
    model = SiteReport
    template_name = "core/sitereport_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = SiteReport.objects.all()
        context['site'] = Site.objects.get(id=self.kwargs['pk'])
        context['project'] = Project.objects.get(sites=self.kwargs['pk'])
        return context


def read_notification(request):
    if request.is_ajax():
        notification = Notification.objects.filter(user=request.user)
        for item in notification:
            notification.update(read=True)
        return JsonResponse({'count':0})
    else:
        notification = Notification.objects.filter(user=request.user, read=False)
        return JsonResponse({'count':notification.count})        


class SubstepReportCreateView(CreateView):
    model = SubstepReport
    form_class = SubstepReportForm
    template_name = "core/substepreport_form.html"

    def get_success_url(self):
        site_id = Site.objects.get(reports=self.object.pk).id
        success_url = reverse_lazy('core:substep_report_list', args=[site_id],) 
        return success_url


class SubstepReportUpdateView(UpdateView):
    model = SubstepReport
    fields = ('user', 'site', 'step', 'substep' 'comment', 'photo')
    template_name = "core/substepreport_form.html"

    def get_success_url(self):
        site_id = Site.objects.get(reports=self.kwargs['pk']).id
        success_url = reverse_lazy('core:substep_report_list', args=[site_id],)
        return success_url


class SubstepReportDeleteView(DeleteView):
    model = SubstepReport
    template_name = "core/substepreport_delete.html"

    def get_success_url(self):
        site_id = Site.objects.get(reports=self.kwargs['pk']).id
        success_url = reverse_lazy('core:substep_report_list', args=[site_id],)
        return success_url


class NotificationView(TemplateView):
    template_name = "core/notification_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notification = Notification.objects.all().order_by('-pk')
        rep_dict = {}
        rep_list = []
        for item in notification:
            rep_dict['notif'] = item
            rep_dict['pk'] = item.report_id
            rep_list.append(dict(rep_dict))
        context['notifications'] = rep_list
        return context


class ReportFeedbackView(CreateView):
    model = ReportFeedback
    form_class = ReportFeedbackForm
    template_name = "core/report_feedback.html"

    def form_valid(self, form):
        form.instance.report = get_object_or_404(SubstepReport, id=self.kwargs['pk'])
        form.instance.user = self.request.user

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = SubstepReport.objects.filter(id=self.kwargs['pk'])
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        success_url = reverse_lazy('core:substep_report_detail', args=[self.kwargs['pk']])
        return success_url


class UserProfileView(CreateView):
    
    template_name = "core/user_profile.html"
    model = User
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['pk'])
        if self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project_id'] = Project.objects.get(project_roles__user=self.request.user).pk
            return context
        return context
        

class SiteDocumentFormView(DocumentRoleMixin, FormView):
    """
    Site Document Form
    """
    form_class = SiteDocumentForm
    template_name = 'core/sitedocument_form.html'

    def post(self, request, *args, **kwargs):
        site = get_object_or_404(Site, pk=self.kwargs['site_id'])

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        doc = request.POST.get('document_name')
        if form.is_valid():
            for file in files:
                SiteDocument.objects.create(file=file, site=site, document_name=doc)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])
        context['project'] = Project.objects.get(sites=self.kwargs['site_id'])
        return context

    def get_success_url(self):
        success_url = reverse_lazy('core:document_list', args=(self.kwargs['site_id'],))
        return success_url


class SiteDocumentListView(DocumentRoleMixin, ListView):
    """
        List of Site Documents
    """
    model = SiteDocument
    template_name = "core/sitedocument_list.html"
    form_class = SiteDocumentForm
    context_object_name = 'documents'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        return SiteDocument.objects.filter(site=self.kwargs['site_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])
        context['project'] = Project.objects.get(sites=self.kwargs['site_id'])
        return context


class SiteDocumentDeleteView(DocumentRoleMixin, DeleteView):
    """
        Delete Site Document
    """
    model = SiteDocument
    form_class = SiteDocumentForm

    def get_success_url(self):
        success_url = reverse_lazy('core:document_list', args=(self.object.site.id,))
        return success_url

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(site_document=self.kwargs['pk'])
        context['project'] = Project.objects.get(sites__site_document=self.kwargs['pk'])
        return context

    
class UserProfileUpdateView(UpdateView):
    """
    User Profile Update View
    """

    template_name = "core/user_profile.html"
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        if not self.request.group.name == 'Super Admin':
            context['project_id'] = self.request.project.pk
        return context


class UserProfileDetailView(DetailView):
    """
    User Profile detail view
    """
    template_name = "core/user_profile_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs['pk'])
        if self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.get(project_roles__user=self.request.user)
            return context
        return context


# updated views

class ConfigureProjectSteps(CreateView):
    model = ConstructionSteps
    fields = ('name', 'name_de', 'order', 'image', 'icon')
    template_name = 'core/configure_project_steps_form.html'

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.kwargs['project_id'])

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('core:project_dashboard', args=(self.kwargs['project_id'],))


class ConfigureSiteSteps(CreateView):
    model = ConstructionSteps
    fields = ('name', 'name_de', 'order', 'image', 'icon')
    template_name = 'core/construction_sitesteps_form.html'

    def form_valid(self, form):
        project_id = Project.objects.filter(sites__id=self.kwargs['site_id'])[0].id

        form.instance.project = get_object_or_404(Project, id=project_id)
        form.save()
        
        obj = SiteSteps()
        obj.site = Site.objects.get(id=self.kwargs['site_id'])
        obj.step = ConstructionSteps.objects.get(id=form.instance.id)
        obj.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = Project.objects.filter(sites__id=self.kwargs['site_id'])[0].id
        context['project'] = Project.objects.get(id=project_id)
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('core:site_detail', args=(self.kwargs['site_id'],))


class SiteSubStepCreate(CreateView):
    template_name = 'core/construction_substep_form.html'
    model = ConstructionSubSteps
    form_class = ConstructionSubStepsForm

    def get(self, request, *args, **kwargs):
        self.object = None
        project_id = Project.objects.filter(sites__id=self.kwargs['site_id'])[0].id
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        primary_photo_form = PrimaryPhotoFormset()
        good_photo_form = GoodPhotoFormset()
        bad_photo_form = BadPhotoFormset()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  primary_photo_form=primary_photo_form,
                                  good_photo_form=good_photo_form,
                                  bad_photo_form=bad_photo_form,

                                  ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        primary_photo_form = PrimaryPhotoFormset(self.request.POST, self.request.FILES)
        good_photo_form = GoodPhotoFormset(self.request.POST, self.request.FILES)
        bad_photo_form = BadPhotoFormset(self.request.POST, self.request.FILES)

        if (
                form.is_valid() and primary_photo_form.is_valid() and good_photo_form.is_valid() and bad_photo_form.is_valid()):
            return self.form_valid(form, primary_photo_form, good_photo_form, bad_photo_form)
        else:
            return self.form_invalid(form, primary_photo_form, good_photo_form, bad_photo_form)

    # def get_form(self, form_class=None):
    #     form = super(SiteSubstepCreate, self).get_form(form_class=self.form_class)
    #     form.fields['step'].queryset = form.fields['step'].queryset.filter(project_id=self.kwargs['project_id'])
    #     return form

    def form_valid(self, form, primary_photo_form, good_photo_form, bad_photo_form):
        self.object = form.save(commit=False)
        form.instance.step = get_object_or_404(ConstructionSteps, id=self.kwargs['step_id'])
        project_id = Project.objects.filter(sites__id=self.kwargs['site_id'])[0].id
        form.instance.project = get_object_or_404(Project, id=project_id)

        form.save()

        primary_photo_form.instance = self.object
        primary_photo_form.save()

        good_photo_form.instance = self.object
        good_photo_form.save()

        bad_photo_form.instance = self.object
        bad_photo_form.save()

        return super(SiteSubStepCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = Project.objects.filter(sites__id=self.kwargs['site_id'])[0].id
        context['project'] = Project.objects.get(id=project_id)
        return context

    def form_invalid(self, form, primary_photo_form, good_photo_form, bad_photo_form):

        return self.render_to_response(
            self.get_context_data(form=form, primary_photo_form=primary_photo_form, good_photo_form=good_photo_form, bad_photo_form=bad_photo_form))

    def get_success_url(self):
        return reverse_lazy('core:site_detail', args=(self.kwargs['site_id'],))


class ConstructionStepUpdate(UpdateView):
    model = ConstructionSteps
    fields = ('name', 'name_de', 'order', 'image', 'icon')
    template_name = 'core/configure_project_steps_form.html'

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.object.project.id)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        step = context['object']
        project = step.project
        # site = step.site
        if project:
            context['project'] = project
        else:
            context['project'] = step.project
        return context

    def get_success_url(self):
        return reverse_lazy('core:project_dashboard', args=(self.object.project.id,))


class ConstructionStepList(TemplateView):
    template_name = 'core/configure_steps_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['construction_steps_list'] = ConstructionSteps.objects.filter(project_id=self.kwargs['project_id']).order_by('order')

        return context


class ConstructionStepDelete(DeleteView):
    model = ConstructionSteps
    template_name = 'core/construction_step_delete.html'

    def get_success_url(self):
        return reverse_lazy('core:project_dashboard', args=(self.object.project.id,))


class ConstructionSubstepCreate(CreateView):
    template_name = 'core/construction_substep_form.html'
    model = ConstructionSubSteps
    form_class = ConstructionSubStepsForm

    def get(self, request, *args, **kwargs):
        self.object = None
        project_id = self.kwargs['project_id']
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        primary_photo_form = PrimaryPhotoFormset()
        good_photo_form = GoodPhotoFormset()
        bad_photo_form = BadPhotoFormset()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  primary_photo_form=primary_photo_form,
                                  good_photo_form=good_photo_form,
                                  bad_photo_form=bad_photo_form,
                                  project_id=project_id

                                  ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        primary_photo_form = PrimaryPhotoFormset(self.request.POST, self.request.FILES)
        good_photo_form = GoodPhotoFormset(self.request.POST, self.request.FILES)
        bad_photo_form = BadPhotoFormset(self.request.POST, self.request.FILES)

        if (
                form.is_valid() and primary_photo_form.is_valid() and good_photo_form.is_valid() and bad_photo_form.is_valid()):
            return self.form_valid(form, primary_photo_form, good_photo_form, bad_photo_form)
        else:
            return self.form_invalid(form, primary_photo_form, good_photo_form, bad_photo_form)

    # def get_form(self, form_class=None):
    #     form = super(ConstructionSubstepCreate, self).get_form(form_class=self.form_class)
    #     form.fields['step'].queryset = form.fields['step'].queryset.filter(project_id=self.kwargs['project_id'])
    #     return form

    def form_valid(self, form, primary_photo_form, good_photo_form, bad_photo_form):
        self.object = form.save(commit=False)
        form.instance.step = get_object_or_404(ConstructionSteps, id=self.kwargs['step_id'])
        form.instance.project = get_object_or_404(Project, id=self.kwargs['project_id'])

        form.save()

        primary_photo_form.instance = self.object
        primary_photo_form.save()

        good_photo_form.instance = self.object
        good_photo_form.save()

        bad_photo_form.instance = self.object
        bad_photo_form.save()

        return super(ConstructionSubstepCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        return context

    def form_invalid(self, form, primary_photo_form, good_photo_form, bad_photo_form):

        return self.render_to_response(
            self.get_context_data(form=form, primary_photo_form=primary_photo_form, good_photo_form=good_photo_form, bad_photo_form=bad_photo_form))

    def get_success_url(self):
        return reverse_lazy('core:project_dashboard', args=(self.kwargs['project_id'],))


# class ConstructionSubstepChoose(CreateView):
#     model = ConstructionSubSteps
#     template_name = "core/construction_sub_steps_choice.html"
#     form_class = ConstructionSubStepsChoiceForm

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)

#         return self.render_to_response(
#             self.get_context_data(form=form))

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)

#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         form.instance.title = self.object.title
#         form.instance.description = self.object.description
#         form.instance.order = self.object.order
#         form.instance.created_by = self.object.created_by
#         form.instance.good_photo = self.object.good_photo
#         form.instance.bad_photo = self.object.bad_photo
#         form.instance.primary_photos.set(self.object.primary_photos)
#         form.instance.step = get_object_or_404(ConstructionSteps, id=self.kwargs['step_id'])
#         form.instance.project = get_object_or_404(Project, id=self.kwargs['project_id'])

#         form.save()

#         return super(ConstructionSubstepChoose, self).form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['project'] = Project.objects.get(id=self.kwargs['project_id'])
#         return context

#     def form_invalid(self, form):

#         return self.render_to_response(
#             self.get_context_data(form=form))

#     def get_success_url(self):
#         return reverse_lazy('core:project_dashboard', args=(self.kwargs['project_id'],))


class ConstructionSubstepsDetail(DetailView):
    template_name = "core/construction_substeps_detail.html"
    form_class = ConstructionSubStepsForm
    model = ConstructionSubSteps


class ConstructionSubstepsUpdate(UpdateView):
    template_name = 'core/construction_substep_form.html'
    model = ConstructionSubSteps
    form_class = ConstructionSubStepsForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        primary_photo_form = PrimaryPhotoFormset(instance=self.object)
        good_photo_form = GoodPhotoFormset(instance=self.object)
        bad_photo_form = BadPhotoFormset(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  primary_photo_form=primary_photo_form,
                                  good_photo_form=good_photo_form,
                                  bad_photo_form=bad_photo_form

                                  ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        primary_photo_form = PrimaryPhotoFormset(self.request.POST, self.request.FILES, instance=self.object)
        good_photo_form = GoodPhotoFormset(self.request.POST, self.request.FILES, instance=self.object)
        bad_photo_form = BadPhotoFormset(self.request.POST, self.request.FILES, instance=self.object)


        if (
                form.is_valid() and primary_photo_form.is_valid() and good_photo_form.is_valid() and bad_photo_form.is_valid()):
            return self.form_valid(form, primary_photo_form, good_photo_form, bad_photo_form)
        else:
            return self.form_invalid(form, primary_photo_form, good_photo_form, bad_photo_form)

    def form_valid(self, form, primary_photo_form, good_photo_form, bad_photo_form):
        self.object = form.save()
        primary_photo_form.instance = self.object
        primary_photo_form.save()

        good_photo_form.instance = self.object
        good_photo_form.save()

        bad_photo_form.instance = self.object
        bad_photo_form.save()

        return super(ConstructionSubstepsUpdate, self).form_valid(form)

    def form_invalid(self, form, primary_photo_form, good_photo_form, bad_photo_form):

        return self.render_to_response(
            self.get_context_data(form=form,
                                  primary_photo_form=primary_photo_form,
                                  good_photo_form=good_photo_form,
                                  bad_photo_form=bad_photo_form

                                  ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        step = context['object']
        project = step.project
        # site = step.site
        if project:
            context['project'] = project
        else:
            context['project'] = step.project
        return context

    def get_success_url(self):
        success_url = reverse_lazy('core:construction_substeps_detail', args=(self.object.pk,))
        return success_url


class ConstructionSitetepsList(TemplateView):
    template_name = "core/construction_site_steps_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checked_steps = SiteSteps.objects.filter(site_id=self.kwargs['site_id']).values('step__name').distinct()
        unchecked_steps = ConstructionSteps.objects.filter(project_id=1).values('name')
        context['checked_steps'] = checked_steps
        context['unchecked_steps'] = unchecked_steps.difference(checked_steps)
        context['site'] = get_object_or_404(Site, id=self.kwargs['site_id'])
        context['site_steps'] = SiteSteps.objects.filter(site_id=self.kwargs['site_id']).order_by('step__order')

        return context


class ConstructionSubstepsDelete(DeleteView):
    model = ConstructionSubSteps
    template_name = 'core/construction_substep_delete.html'

    def get_success_url(self):
        success_url = reverse_lazy('core:project_dashboard', args=(self.object.project.pk,))
        return success_url


class ConstructionSiteStepsDelete(DeleteView):
    model = SiteSteps
    template_name = 'core/construction_site_steps_delete.html'

    def get_success_url(self):
        success_url = reverse_lazy('core:site_detail', args=(self.object.site.pk,))
        return success_url


class ChecklistCreateView(CreateView):
    template_name = 'core/checklist_form.html'
    model = NewCommonSubStepChecklist
    form_class = NewCommonChecklistForm

    def get(self, request, *args, **kwargs):
        self.object = None
        # project_id = self.kwargs['project_id']
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        checklist_formset = NewChecklistFormset()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  checklist_formset=checklist_formset
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        checklist_formset = NewChecklistFormset(self.request.POST)
        

        if (
                form.is_valid() and checklist_formset.is_valid()):
            return self.form_valid(form, checklist_formset)
        else:
            return self.form_invalid(form, checklist_formset)

    # def get_form(self, form_class=None):
    #     form = super(ConstructionSubstepCreate, self).get_form(form_class=self.form_class)
    #     form.fields['step'].queryset = form.fields['step'].queryset.filter(project_id=self.kwargs['project_id'])
    #     return form

    def form_valid(self, form, checklist_formset):
        self.object = form.save(commit=False)
        form.instance.site = get_object_or_404(Site, id=self.kwargs['site_id'])
        form.instance.substep = get_object_or_404(ConstructionSubSteps, id=self.kwargs['substep_id'])
        form.instance.step = get_object_or_404(SiteSteps, id=self.kwargs['step_id'])

        form.save()

        checklist_formset.instance = self.object
        checklist_formset.save()

        return super(ChecklistCreateView, self).form_valid(form)

    def form_invalid(self, form, checklist_formset):

        return self.render_to_response(
            self.get_context_data(form=form, checklist_formset=checklist_formset))
 
    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])
        context['project'] = Project.objects.get(sites=self.kwargs['site_id'])
        return context

    def get_success_url(self):
        success_url = reverse_lazy('core:checklist', args=(self.kwargs['site_id'],self.kwargs['step_id'], self.kwargs['substep_id']))
        return success_url

# class ChecklistCreateView(CreateView):
#     model = NewCommonSubStepChecklist
#     template_name = 'core/checklist_form.html'
#     form_class = NewCommonChecklistForm

#     # def get_form(self, form_class=None):
#     #     form = super(ChecklistCreateView, self).get_form(form_class=self.form_class)
#     #     form.fields['step'].queryset = form.fields['step'].queryset.filter(site_id=self.kwargs['site_id'])
#     #     return form

#     def form_valid(self, form):
#         form.instance.site = get_object_or_404(Site, pk=self.kwargs['site_id'])
#         form.save()
#         return super().form_valid(form)

#     def get_context_data(self, *, object_list=None, **kwargs):

#         context = super().get_context_data(**kwargs)
#         context['site'] = Site.objects.get(id=self.kwargs['site_id'])
#         context['project'] = Project.objects.get(sites=self.kwargs['site_id'])
#         return context

#     def get_success_url(self):
#         success_url = reverse_lazy('core:site_detail', args=(self.kwargs['site_id'],))
#         return success_url


class ChecklistUpdateView(UpdateView):
    model = NewCommonSubStepChecklist
    template_name = "core/checklist_form.html"
    form_class = NewCommonChecklistForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        checklist_formset = NewChecklistFormset(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  checklist_formset=checklist_formset
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        Formset = inlineformset_factory(NewCommonSubStepChecklist, NewSubStepChecklist, fields=['title', ], extra=0)
        checklist_formset = Formset(self.request.POST, instance=self.object)
        

        if (
                form.is_valid() and checklist_formset.is_valid()):
            return self.form_valid(form, checklist_formset)
        else:
            return self.form_invalid(form, checklist_formset)

    def form_valid(self, form, checklist_formset):
        self.object = form.save(commit=False)
        form.instance.site = get_object_or_404(Site, id=self.object.site.id)
        form.instance.substep = get_object_or_404(ConstructionSubSteps, id=self.object.substep.id)
        form.instance.step = get_object_or_404(SiteSteps, id=self.object.step.id)

        self.object.save()

        checklist_formset.instance = self.object
        checklist_formset.save()

        return super(ChecklistUpdateView, self).form_valid(form)

    def form_invalid(self, form, checklist_formset):

        return self.render_to_response(
            self.get_context_data(form=form, checklist_formset=checklist_formset))

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(id=self.object.site.id)
        context['project'] = Project.objects.get(sites=self.object.site.id)
        return context

    def get_success_url(self):
        success_url = reverse_lazy('core:checklist', args=(self.object.site.id, self.object.step.id, self.object.substep.id))
        return success_url


class ChecklistDeleteView(DeleteView):
    model = NewCommonSubStepChecklist
    template_name = "core/checklist_delete_form.html"

    def get_success_url(self):
        success_url = reverse_lazy('core:checklist', args=(self.object.site.id, self.object.step.id, self.object.substep.id))
        return success_url


class ChecklistView(ListView):
    model = NewCommonSubStepChecklist
    template_name = 'core/substep_checklist.html'
    context_object_name = 'checklists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])
        context['project'] = Project.objects.get(sites=self.kwargs['site_id'])
        context['substep_id'] = self.kwargs['substep_id']
        context['step_id'] = self.kwargs['step_id']
        return context


    def get_queryset(self):
        return NewCommonSubStepChecklist.objects.filter(substep_id=self.kwargs['substep_id'], site_id=self.kwargs['site_id']).prefetch_related('sub_checklists')



class CheckListAllView(TemplateView):
    model = NewCommonSubStepChecklist
    template_name = 'core/checklist_all.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # site_id = get_object_or_404(Site, id=self.kwargs['site_id'])
        context = super().get_context_data(**kwargs)
        # context['checklists'] = SubStepCheckList.objects.filter(site_id=site_id)

        checklist_all = NewCommonSubStepChecklist.objects.filter(site_id=self.kwargs['site_id']).prefetch_related('sub_checklists')
        paginator = Paginator(checklist_all, 10)  # Show 10 checklist per page

        page = self.request.GET.get('page')
        checklists = paginator.get_page(page)
        context['checklists_lists'] = checklists
        return context

# def export(request):
#     output = []
#     response = HttpResponse(content_type='application/xls')
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8'))
#     query_set = NewSubStepChecklist.objects.all()
#     # Header
#     writer.writerow(['Title', 'Sub Checklist', 'Status'])
#     for query in query_set:
#         writer.writerow([query.title, query.common_checklist, query.status])
#     # CSV Data
#     return response

def export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('NewSubStepChecklist')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Title', 'Sub Checklist', 'Status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = NewSubStepChecklist.objects.all().values_list('title', 'common_checklist__title', 'status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def ExportChecklistPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="download.pdf"'

    p = canvas.Canvas(response)
    query_set = NewSubStepChecklist.objects.all()
    count = 0
    for qs in query_set:
        y = 900 - count * 100
        p.drawString(0, y-20, "Title: " + qs.title)
        p.drawString(0, y, "Sub Checklist: " + qs.common_checklist.title)
        p.drawString(0, y+20, "Status: " + str(qs.status))
        count = count + 1

    p.showPage()
    p.save()
    return response


class HousesAndGeneralConstructionMaterialsListView(ListView):
    model = HousesAndGeneralConstructionMaterials
    template_name = "core/house_general_construction_materials_list.html"


class HousesAndGeneralConstructionMaterialsDetailView(DetailView):
    model = HousesAndGeneralConstructionMaterials
    temlate_name = "core/house_general_construction_materials_detail.html"


class HousesAndGeneralConstructionMaterialsCreateView(CreateView):
    model = HousesAndGeneralConstructionMaterials
    form_class = HousesAndGeneralConstructionMaterialsForm
    template_name = "core/house_general_construction_materials_form.html"
    success_url = reverse_lazy('core:house_general_construction_materials_list')


class HousesAndGeneralConstructionMaterialsUpdateView(UpdateView):
    model = HousesAndGeneralConstructionMaterials
    fields = ('name', 'good_photo', 'good_photo_desc', 'bad_photo', 'bad_photo_desc',)
    template_name = "core/house_general_construction_materials_form.html"
    success_url = reverse_lazy('core:house_general_construction_materials_list')


class HousesAndGeneralConstructionMaterialsDeleteView(DeleteView):
    model = HousesAndGeneralConstructionMaterials
    template_name = "core/house_general_construction_materials_delete.html"
    success_url = reverse_lazy('core:house_general_construction_materials_list')


class BuildHouse(TemplateView):
    template_name = 'core/build_house.html'


class MakeHouseStrongListView(ListView):
    model = BuildAHouseMakesHouseStrong
    template_name = "core/make_house_strong_list.html"


class MakesHouseStrongDetailView(DetailView):
    model = BuildAHouseMakesHouseStrong
    temlate_name = "core/make_house_strong_detail.html"


class MakesHouseStrongCreateView(CreateView):
    model = BuildAHouseMakesHouseStrong
    form_class = BuildAHouseMakesHouseStrongForm
    template_name = "core/make_house_strong_form.html"
    success_url = reverse_lazy('core:make_house_strong_list')


class MakesHouseStrongUpdateView(UpdateView):
    model = BuildAHouseMakesHouseStrong
    fields = ('name', 'pdf',)
    template_name = "core/make_house_strong_form.html"
    success_url = reverse_lazy('core:make_house_strong_list')


class MakesHouseStrongDeleteView(DeleteView):
    model = BuildAHouseMakesHouseStrong
    template_name = "core/make_house_strong_delete.html"
    success_url = reverse_lazy('core:make_house_strong_list')


class KeyPartsOfHouseListView(ListView):
    model = BuildAHouseKeyPartsOfHouse
    template_name = "core/key_parts_house_list.html"


class KeyPartsOfHouseDetailView(DetailView):
    model = BuildAHouseKeyPartsOfHouse
    template_name = "core/key_parts_house_detail.html"


class KeyPartsOfHouseCreateView(CreateView):
    model = BuildAHouseKeyPartsOfHouse
    form_class = BuildAHouseKeyPartsOfHouseForm
    template_name = "core/key_parts_house_form.html"
    success_url = reverse_lazy('core:key_parts_house_list')


class KeyPartsOfHouseUpdateView(UpdateView):
    model = BuildAHouseKeyPartsOfHouse
    fields = ('name', 'good_photo', 'good_photo_desc', 'bad_photo', 'bad_photo_desc',)
    template_name = "core/key_parts_house_form.html"
    success_url = reverse_lazy('core:key_parts_house_list')


class KeyPartsOfHouseDeleteView(DeleteView):
    model = BuildAHouseKeyPartsOfHouse
    template_name = "core/key_parts_house_delete.html"
    success_url = reverse_lazy('core:key_parts_house_list')



def report_photo_delete(request, pk):
    report_obj=get_object_or_404(SubstepReport, id=pk)
    report_obj.photo.delete()
    report_obj.save()
    messages.success(request, "Successfully deleted")

    return HttpResponseRedirect(reverse('core:substep_report_detail', args=[pk]))





