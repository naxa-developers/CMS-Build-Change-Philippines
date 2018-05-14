from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core.models import Step, Checklist

class StepSerializer(serializers.ModelSerializer):
    localname = serializers.ReadOnlyField(source="get_localname")
    class Meta:
        model = Step
        fields = ('name', 'site', 'project', 'order','localname',)

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
    class Meta:
        model = Checklist
        fields = ('text', )

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