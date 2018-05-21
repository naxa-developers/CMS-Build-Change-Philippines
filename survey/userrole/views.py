from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, RedirectView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from core.models import Project, Site
from core.views import SuperAdminMixin, ProjectManagerMixin

from .models import UserRole
from .forms import UserRoleForm


class Redirection(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        try:
            if self.request.user.user_roles.filter(group__name='Super Admin'):
                return reverse("core:admin_dashboard")
            elif self.request.user.user_roles.filter(group__name='Project Manager'):
                project_id = Project.objects.get(project_roles__user=self.request.user).pk
                return reverse_lazy("core:project_dashboard", kwargs={'project_id': project_id})
        except:
            return reverse("login")


class UserRoleCreateView(SuperAdminMixin, CreateView):
    """
    Project Manager
    """
    model = UserRole
    form_class = UserRoleForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            group = Group.objects.get(name='Project Manager')
            user = form.cleaned_data['user']
            project = Project.objects.get(id=kwargs['project_id'])
            UserRole.objects.get_or_create(user=user, group=group, project=project)
            return redirect('core:admin_dashboard')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
        return context


class FieldEngineerUserRoleFormView(ProjectManagerMixin, CreateView):
    """
    Field Engineer
    """
    model = UserRole
    form_class = UserRoleForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            group = Group.objects.get(name='Field Engineer')
            user = form.cleaned_data['user']
            UserRole.objects.get_or_create(user=user, group=group, site_id=self.kwargs['site_id'])
            return redirect('core:project_dashboard')

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.select_related().get(id=self.kwargs['site_id'])

        if self.request.user.user_roles.filter(group__name="Super Admin"):
            context['projects'] = Project.objects.all()
            return context
        elif self.request.user.user_roles.filter(group__name="Project Manager"):
            context['project'] = Project.objects.filter(project_roles__user=self.request.user)
        return context
