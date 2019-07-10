from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, RedirectView, ListView, FormView, TemplateView, UpdateView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect

from core.models import Project, Site
from core.views import SuperAdminMixin, ManagerSuperAdminMixin
from .models import UserRole, FieldEngineerProfile
from .forms import AssignProjectManagerForm, AssignFieldEnginnerForm, ProjectUserForm, SendInvitationForm, FieldEngineerForm


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


class AssignProjectManagerView(ManagerSuperAdminMixin, CreateView):
    """
    Project Manager
    """
    model = UserRole
    form_class = AssignProjectManagerForm
    template_name = "userrole/userrole_create_form.html"

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            # unassigned_group = Group.objects.get(name='Unassigned')
            user = form.cleaned_data['user']

            project = Project.objects.get(id=kwargs['project_id'])
            project_manager_group = Group.objects.get(name='Project Manager')
            UserRole.objects.filter(user=user, project=project).update(group=project_manager_group)
            return redirect('core:project_dashboard', project_id=self.kwargs['project_id'])

        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_id'])

        return context

    def get_form(self, form_class=None):
        form = super(AssignProjectManagerView, self).get_form(form_class=self.form_class)
        form.fields['user'].queryset = form.fields['user'].queryset.filter(user_roles__project_id=self.kwargs['project_id']).\
            exclude(user_roles__group__name="Project Manager")

        return form


class FieldEngineerUserRoleFormView(ManagerSuperAdminMixin, CreateView):
    """
    Assign Field Engineer
    """
    model = UserRole
    form_class = AssignFieldEnginnerForm
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
        form.fields['user'].queryset = form.fields['user'].queryset.filter(user_roles__project_id=project_id.id,
                                                                           user_roles__group__name="Field Engineer")
        return form


class FieldEngineerCreate(CreateView):
    template_name = 'userrole/field_engineer_form.html'

    def get(self, request, *args, **kwargs):
        form = FieldEngineerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FieldEngineerForm(data=request.POST)
        if form.is_valid():
            project_id = self.kwargs['project_id']
            print(project_id)
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            UserRole.objects.get_or_create(user=user, group=Group.objects.get(name='Field Engineer'), project_id=project_id)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            FieldEngineerProfile.objects.create(user=user, first_name=first_name, last_name=last_name, email=email,
                                                phone_number=phone_number)

            return redirect(reverse('core:project_dashboard', kwargs={'project_id': self.kwargs['project_id']}))

        return render(request, self.template_name, {'form': form})


# class FieldEngineerDelete(DeleteView):
#     template_name = 'userrole/field_engineer_delete.html'
#     success_url = reverse_lazy('core:site_detail')


class ProjectUserFormView(CreateView):
    model = User
    template_name = 'userrole/project_user_form.html'
    form_class = ProjectUserForm

    def post(self, request, *args, **kwargs):
        form = ProjectUserForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            phone_number = form.cleaned_data['phone_number']
            user.save()

            UserRole.objects.create(user=user, group=Group.objects.get(name='Unassigned'),
                                    project_id=self.kwargs['project_id'], extra={'phone_number': phone_number})
            return redirect(reverse('userrole:thankyou'))

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


class SendInvitationView(ManagerSuperAdminMixin, SuccessMessageMixin, FormView):
    model = User
    form_class = SendInvitationForm
    template_name = 'userrole/send_email_invitation.html'

    def form_valid(self, form):
        user_exists = UserRole.objects.filter(user__email=form.cleaned_data['email'],\
                                   group=Group.objects.get(name='Unassigned'),
                                   project__id=self.kwargs['project_id']).exists()
        print(user_exists)
        if not user_exists:
            status = form.send_email()
            print(status)
            print(status)
            if status == 1:
                messages.success(self.request, "Invitation Sent To {}!".format(form.cleaned_data['email']))
            else:
                messages.error(self.request, "Invitation to {} Unsuccessful.".format(form.cleaned_data['email']))
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, data="Sorry! The user already exists."))

    def get_form_kwargs(self):
        kwargs = super(SendInvitationView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'project': self.kwargs['project_id']
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['project'] = Project.objects.get(id=self.kwargs['project_id'])
        return context

    def get_success_url(self):
        success_url = reverse_lazy('core:project_dashboard',  args=(self.kwargs['project_id'],))
        return success_url


class Thankyou(TemplateView):
    template_name = "userrole/thankyou.html"


class RoleDelete(DeleteView):
    model = UserRole
    template_name = "userrole/role_delete.html"

    def get_success_url(self):
        success_url = reverse_lazy('core:site_detail',  args=(self.object.site.id,))
        return success_url


class AssignProjectManagerPhoneNumber(TemplateView):
    template_name = "userrole/assign_phone_number.html"

    def get(self, request, **kwargs):
        print(self.kwargs['pk'])
        obj = get_object_or_404(UserRole, id=self.kwargs['pk'])
        context = {}
        context['project_manager'] = obj.user.username
        if obj.extra:
            context['phone_number'] = obj.extra['phone_number']

        return super(AssignProjectManagerPhoneNumber, self).render_to_response(context)

    def post(self, request, **kwargs):
        obj = get_object_or_404(UserRole, id=self.kwargs['pk'])
        if obj:
            data = request.POST
            phone_number = data['phone_number']
            obj.extra = {'phone_number':phone_number}
            obj.save()
            messages.success(request, 'successfully added phone number')
            return HttpResponseRedirect(reverse('userrole:assign_phone_number', args=[self.kwargs['pk']]))

        context = {}
        return super(AssignProjectManagerPhoneNumber, self).render_to_response(context)
