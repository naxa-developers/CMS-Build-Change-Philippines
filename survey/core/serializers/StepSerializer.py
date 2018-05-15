from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core.models import Step, Checklist, Material

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
        # import pdb; pdb.set_trace();
        
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
        materials = obj.checklist_material.all()
        serializer = MaterialSerializer(instance=materials, many=True)
        return serializer.data 

    def create(self, validated_data):
        # import pdb; pdb.set_trace();
        
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