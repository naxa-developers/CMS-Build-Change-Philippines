from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, RedirectView, ListView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Project, Site
from core.views import SuperAdminMixin, ProjectManagerMixin, ManagerSuperAdminMixin

from .models import UserRole
from .forms import UserRoleForm, ProjectUserForm


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
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])

        return context


class FieldEngineerUserRoleFormView(ManagerSuperAdminMixin, CreateView):
    """
    Field Engineer
    """
    model = UserRole
    form_class = UserRoleForm
    template_name = 'userrole/userrole_form.html'

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            group = Group.objects.get(name='Field Engineer')
            user = form.cleaned_data['user']
            UserRole.objects.get_or_create(user=user, group=group, site_id=self.kwargs['site_id'])
            return redirect(reverse('core:site_detail', kwargs={'pk': self.kwargs['site_id']}))

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = Site.objects.get(id=self.kwargs['site_id'])
        context['project'] = Project.objects.get(sites=self.kwargs['site_id'])

        return context

    def get_form(self, form_class=None):
        form = super(FieldEngineerUserRoleFormView, self).get_form(form_class=self.form_class)
        project_id = Project.objects.get(sites=self.kwargs.get('site_id'))
        form.fields['user'].queryset = form.fields['user'].queryset.filter(user_roles__project_id=project_id.id)
        return form


class ProjectUserFormView(ManagerSuperAdminMixin, CreateView):
    model = User
    template_name = 'userrole/project_user_form.html'
    form_class = ProjectUserForm

    def post(self, request, *args, **kwargs):
        form = ProjectUserForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            UserRole.objects.create(user=user, group=Group.objects.get(name='Unassigned'),
                                    project_id=self.kwargs['project_id'])
            return redirect(reverse('core:project_dashboard', kwargs={'project_id': self.kwargs['project_id']}))

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        return context


class ProjectUserListView(ManagerSuperAdminMixin, ListView):
    model = User
    template_name = 'userrole/project_user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_id'])
        context['users'] = User.objects.filter(user_roles__project_id=self.kwargs.get('project_id'))
        if self.request.user.user_roles.filter(group__name="Super Admin"):
            if not self.kwargs['project_id']:
                context['projects'] = Project.objects.all()
                return context
        return context

