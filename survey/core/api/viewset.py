from django.contrib.auth.models import User

from rest_framework import viewsets, serializers, mixins

from core.models import Project, Step
from .serializers import ProjectSerializer, StepsSerializer


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('sites', 'sites__steps')


# class StepsViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = StepsSerializer
#     queryset = Step.objects.all()
#

class StepsViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):

    serializer_class = StepsSerializer
    queryset = Step.objects.all()