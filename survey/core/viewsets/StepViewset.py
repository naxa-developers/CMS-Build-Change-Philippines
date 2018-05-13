from rest_framework import routers, serializers, viewsets
from core.serializers.StepSerializer import StepSerializer
from core.models import Step
class StepViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing sites.
    """
    serializer_class = StepSerializer
    
    def get_queryset(self):
        return Step.objects.filter(site = self.kwargs.get('pk'))