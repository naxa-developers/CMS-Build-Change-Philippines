from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.shortcuts import reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.exceptions import PermissionDenied

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from userrole.forms import UserProfileForm
from userrole.models import UserRole
from .models import Project, Site, Category, Material, Step, Report
from .forms import ProjectForm, CategoryForm, MaterialForm


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def token(request):
    user = User.objects.first()
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'email': user.email
    })


class ProjectManagerMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            if request.user.user_roles.filter(group__name="Project Manager"):
                return super(ProjectManagerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied


class SuperAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_roles.filter(group__name="Super Admin"):
                return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied


class ManagerSuperAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_roles.filter(group__name="Super Admin")\
                    or self.request.user.user_roles.filter(group__name="Project Manager"):
                return super(ManagerSuperAdminMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm
    context_object_name = 'projects'

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Project Manager"):
            return reverse('core:project_dashboard')
        elif self.request.user.user_roles.filter(group__name="Super Admin"):
            return reverse('core:admin_dashboard')


class ProjectCreateView(SuperAdminMixin, ProjectMixin, CreateView):
    """
    Project CreateView
    """
    template_name = "core/project_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            context['project_id'] = self.kwargs['project_id']
            return context


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


class ProjectUpdateView(ProjectMixin, UpdateView):
    """
    Project UpdateView
    """
    template_name = "core/project_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            context['project_id'] = self.kwargs['pk']
            return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.user_roles.filter(group__name="Project Manager"):
            try:
                obj = self.get_object()
                user_role = self.request.user.user_roles.get(project_id=self.kwargs['pk'])
                if obj.project_roles.values_list('project__name', flat=True)[0] == user_role.project:
                    return self.get_success_url()
                return super(ProjectUpdateView, self).dispatch(request, *args, **kwargs)
            except UserRole.DoesNotExist:
                raise PermissionDenied
        elif self.request.user.user_roles.filter(group__name="Super Admin"):
            return super(ProjectUpdateView, self).dispatch(request, *args, **kwargs)


class ProjectDeleteView(SuperAdminMixin, ProjectMixin, DeleteView):
    """
    Project DeleteView
    """
    template_name = "core/project_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            context['project_id'] = self.kwargs['pk']
            return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.user_roles.filter(group__name="Project Manager"):
            try:
                obj = self.get_object()
                user_role = self.request.user.user_roles.get(project_id=self.kwargs['pk'])
                if obj.project_roles.values_list('project__name', flat=True)[0] == user_role.project:
                    return self.get_success_url()
                return super(ProjectDeleteView, self).dispatch(request, *args, **kwargs)
            except UserRole.DoesNotExist:
                raise PermissionDenied
        elif self.request.user.user_roles.filter(group__name="Super Admin"):
            return super(ProjectDeleteView, self).dispatch(request, *args, **kwargs)


class UserCreateView(ManagerSuperAdminMixin, CreateView):
    """
    User SignUp form
    """
    form_class = UserProfileForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Project Manager"):
            return reverse('core:project_dashboard')
        elif self.request.user.user_roles.filter(group__name="Super Admin"):
            return reverse('core:admin_dashboard')


class ProjectDashboard(ProjectManagerMixin, TemplateView):
    """
    dashboard for Project Manager
    """

    template_name = "core/project_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(project_roles__user=self.request.user)
        context['project_id'] = Project.objects.filter(project_roles__user=self.request.user).values_list('id',flat=True)[0]
        context['materials_list'] = Project.objects.filter(project_roles__user=self.request.user)\
                                .prefetch_related('material')\
                                .values_list('material__id','material__title','material__category__id',\
                                             'material__category__name',\
                                             'material__good_photo', 'material__bad_photo')
        project = Project.objects.filter(project_roles__user=self.request.user)
        context['if_material'] = Material.objects.filter(project=project[0]).count()
        context['if_category'] = Category.objects.filter(project=project[0]).count()
        context['category_list'] = Project.objects.filter(project_roles__user=self.request.user)\
                                    .prefetch_related('category').values_list('category__id', 'category__name')
        return context


class Dashboard(SuperAdminMixin, TemplateView):
    """
    dashboard for Super Admin
    """
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['latest_project'] = Project.objects.latest('id')
        return context


class SiteCreateView(ManagerSuperAdminMixin, CreateView):
    """
    Site Create Form
    """

    template_name = "core/site_create.html"
    model = Site
    fields = ('name', 'type', 'photo', 'address', 'latitude', 'longitude', 'contact_number',)

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url

        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class SiteListView(ManagerSuperAdminMixin, ListView):
    """
    Site List View
    """

    template_name = "core/site_list.html"
    model = Site
    paginate_by = 100


class SiteDetailView(ManagerSuperAdminMixin, DetailView):
    """
    Site Detail View
    """
    template_name = "core/site_detail.html"
    model = Site

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['step_list'] = Step.objects.filter(site=self.kwargs['pk'])[:2]
        data['site_materials'] = Material.objects.filter(project__sites=self.kwargs['pk'])[:2]
        data['site_reports'] = Report.objects.filter(checklist__step__site=self.kwargs['pk'])[:2]
        print(Report.objects.filter(checklist__step__site=3))
        data['project_id'] = Project.objects.filter(sites=self.kwargs['pk']).values_list('id', flat=True)[0]

        return data


class SiteUpdateView(ManagerSuperAdminMixin, UpdateView):
    """
    Site Update View
    """
    template_name = "core/site_create.html"
    model = Site
    fields = '__all__'

    def form_valid(self, form):
        form.instance.site = get_object_or_404(Site, pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            # context['project_id'] = Site.objects.filter(project=)
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url

        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class SiteDeleteView(ManagerSuperAdminMixin, DeleteView):
    """
    Site Delete View
    """
    model = Site

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            # context['project_id'] = Site.objects.filter(project=)
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url

        elif self.request.user.user_roles.filter(group__name="Project Manager"):
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
        else:
            data['project'] = data['pk']
        return data


class CategoryFormView(ManagerSuperAdminMixin, FormView):
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
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.kwargs['project_id'],))
            return success_url
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class CategoryListView(ManagerSuperAdminMixin, ListView):
    """
    Category ListView
    """
    template_name = "core/category_list.html"
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs['pk']
        context['category_list'] = Category.objects.filter(project=self.kwargs['pk'])
        context['if_category'] = Category.objects.filter(project=self.kwargs['pk']).count()
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            return context


class CategoryUpdateView(ManagerSuperAdminMixin, UpdateView):
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
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            # context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class CategoryDeleteView(ManagerSuperAdminMixin, DeleteView):
    """
    Category DeleteView
    """
    model = Category
    template_name = "core/category_confirm_delete.html"

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url

        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class MaterialFormView(ManagerSuperAdminMixin, FormView):
    """
    Material From View
    """
    template_name = "core/material_form.html"
    form_class = MaterialForm

    def get_form(self, form_class=None):
        form = super(MaterialFormView, self).get_form(form_class=self.form_class)
        form.fields['category'].queryset = form.fields['category'].queryset.filter(project=self.kwargs['project_id'])
        return form

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            context['materials_list'] = Material.objects.filter(project=self.kwargs['project_id'])
            context['if_material'] = Material.objects.filter(project=self.kwargs['project_id']).count()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            context['materials_list'] = Material.objects.filter(project=self.kwargs['project_id'])
            context['if_material'] = Material.objects.filter(project=self.kwargs['project_id']).count()
            context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.kwargs['project_id'],))
            return success_url
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class MaterialUpdateView(ManagerSuperAdminMixin, UpdateView):
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
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            # context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class MaterialDeleteView(ManagerSuperAdminMixin, DeleteView):
    """
    Category DeleteView
    """
    model = Material
    template_name = "core/material_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
            # context['project_id'] = self.kwargs['project_id']
            return context

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.object.project.pk,))
            return success_url

        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_dashboard')
            return success_url


class MaterialDetailView(ManagerSuperAdminMixin, DetailView):
    """
    Category UpdateView
    """
    template_name = "core/material_detail.html"
    model = Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
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
            context['materials_list'] = Material.objects.filter(project=self.kwargs['pk'])
            context['if_material'] = Material.objects.filter(project=self.kwargs['pk']).count()
            context['project_id'] = self.kwargs['pk']
            return context


class ReportListView(ManagerSuperAdminMixin, ListView):
    """
    Report List
    """
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.filter(checklist__step__site=self.kwargs['site_pk'])
        return context


class ReportDetailView(ManagerSuperAdminMixin, DetailView):
    """
    Report detail
    """
    model = Report

