from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .models import UserRole
from .forms import UserRoleForm

from core.models import Project


class UserRoleCreateView(CreateView):
    model = UserRole
    form_class = UserRoleForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            group = Group.objects.get(name='Project Manager')
            user = form.cleaned_data['user']
            project = Project.objects.get(id=kwargs['project_id'])
            UserRole.objects.get_or_create(user=user, group=group, project=project)
            return redirect('core:project_list')

        return render(request, self.template_name, {'form': form})