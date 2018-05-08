from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.shortcuts import reverse

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Project

from .forms import ProjectForm


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


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm
    context_object_name = 'projects'

    def get_success_url(self):
        return reverse('core:project_list')


class ProjectCreateView(ProjectMixin, CreateView):
    pass


class ProjectListView(ProjectMixin, ListView):
    pass


class ProjectDetailView(ProjectMixin, DetailView):
    pass


class ProjectUpdateView(ProjectMixin, UpdateView):
    pass


class ProjectDeleteView(ProjectMixin, DeleteView):
    pass

