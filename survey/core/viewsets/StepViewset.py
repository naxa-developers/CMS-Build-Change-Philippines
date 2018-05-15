from rest_framework import routers, serializers, viewsets
from core.serializers.StepSerializer import StepSerializer, ChecklistSerializer
from core.models import Checklist, Step, Project
class StepViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing sites.
    """
    serializer_class = StepSerializer
    
    def get_queryset(self):
        return Step.objects.filter(site_id = self.kwargs.get('pk'))

    def perform_create(self, serializer, **kwargs):
        # import pdb; pdb.set_trace()
        # project=serializer.validated_data.get('project')
        localname = serializer.initial_data.get('localname', '')
        # try:
        #     if project.setting.local_language:
        #         print ("----------++++++++++---")
        #         import pdb; pdb.set_trace()
        #         setattr(instance, 'name_'+project.setting.local_language, localname)
        #         print (instance.name_de)
        # except:
        #     pass
        data = serializer.save(localname=localname)
        return data

class ChecklistViewset(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing sites.
    """
    serializer_class = ChecklistSerializer
    
    def get_queryset(self):
        return Checklist.objects.filter(step_id = self.kwargs.get('pk'))

    def perform_create(self, serializer, **kwargs):
        localtext = serializer.initial_data.get('localtext', '')
        data = serializer.save(localtext=localtext)
        return data


# {
#     "name": "cv",
#     "site": 1,
#     "project": 1,
#     "order": 1,
# "localname":"dssd"
# }
        