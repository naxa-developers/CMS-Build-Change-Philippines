from rest_framework import serializers
from core.models import Project, Site, Step, Checklist, Material

class StepsSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='sites.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Step
        fields = ('id', 'name', 'order', 'checklist', 'site_name', 'sites', 'project', 'project_name')

    def create(self, validated_data):
        sites = validated_data.pop('sites', None)
        project = validated_data.pop('project', None)
        step = Step.objects.create(**validated_data)
        step.sites = sites
        step.project = project
        step.save()
        return step


class ProjectStepsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = ('id', 'name', 'order', 'checklist')


class SitesSerializer(serializers.ModelSerializer):
    steps = ProjectStepsSerializer(many=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'steps')


class ProjectSerializer(serializers.ModelSerializer):
    sites = SitesSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'sites')



class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        exclude = ()

    
class StepSerializer(serializers.ModelSerializer):
    localname = serializers.ReadOnlyField(source="get_localname")
    class Meta:
        model = Step
        fields = ('id','name', 'site', 'project', 'order','localname',)

    def create(self, validated_data):
        localname = validated_data.pop('localname') if 'localname' in validated_data else ""
        instance = Step.objects.create(**validated_data)
        project = instance.site.project
        try:
            if project.setting.local_language:
                setattr(instance, 'name_'+project.setting.local_language, localname)
        except:
            pass
        instance.save()
        return instance

class ChecklistSerializer(serializers.ModelSerializer):
    localtext = serializers.ReadOnlyField(source="get_localtext")
    materials = serializers.SerializerMethodField()
    class Meta:
        model = Checklist
        fields = ('id', 'text', 'step', 'localtext', 'materials',)

    def get_materials(self, obj):
        serializer = MaterialSerializer(instance=obj.material, many=False)
        return serializer.data 

    def create(self, validated_data):
        localname = validated_data.pop('localtext') if 'localtext' in validated_data else ""
        instance = Checklist.objects.create(**validated_data)
        project = instance.step.project
        
        try:
            if project.setting.local_language:
                setattr(instance, 'text_'+project.setting.local_language, localname)
        except:
            pass
        instance.save()
        return instance