from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView, ListView
from django.shortcuts import reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.exceptions import PermissionDenied

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from userrole.models import UserRole

from .models import Project, Site, Category
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

            if request.user.user_roles.filter(group__name="Super Admin") or request.user.user_roles.filter(group__name="Project Manager"):
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
    pass


class ProjectDetailView(SuperAdminMixin, ProjectMixin, DetailView):
    pass


class ProjectUpdateView(ProjectMixin, UpdateView):

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
    pass


class UserCreateView(SuperAdminMixin, FormView):
    """
    User SignUp form for Super Admin
    """
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('core:project_list')


class ProjectDashboard(ProjectManagerMixin, TemplateView):
    """
    dashboard for Project Manager
    """

    template_name = "core/project_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.filter(project_roles__user=self.request.user)
        return context


class Dashboard(SuperAdminMixin, TemplateView):
    """
    dashboard for Super Admin
    """
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context


class SiteCreateView(ManagerSuperAdminMixin, CreateView):
    """
    Site Create Form
    """

    template_name = "core/site_create.html"
    model = Site
    fields = ('name', 'type', 'photo', 'address', 'latitude', 'longitude', 'contact_number',)

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return super().form_valid(form)

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
    template_name = "core/project_detail.html"
    model = Site

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

    def get_context_data(self, **kwargs):
        data = super(SiteStepsView, self).get_context_data(**kwargs)
        return data


class CategoryFormView(ManagerSuperAdminMixin, FormView):
    """
    Category Form View
    """
    template_name = "core/category_create.html"
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.kwargs['pk'],))
            return success_url
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_detail')
            return success_url


class MaterialFormView(ManagerSuperAdminMixin, FormView):
    """
    Material From View
    """
    template_name = "core/material_form.html"
    form_class = MaterialForm

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            success_url = reverse_lazy('core:project_detail', args=(self.kwargs['pk'],))
            return success_url
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            success_url = reverse_lazy('core:project_detail')
            return success_url