from rest_framework import serializers

from core.models import Project, Site, Step


class StepsSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='sites.name', read_only=True)
    # site_name = serializers.CharField(source='sites.name')
    project_name = serializers.CharField(source='sites.project.name', read_only=True)

    class Meta:
        model = Step
        fields = ('id', 'name', 'order', 'checklist', 'site_name', 'sites', 'project', 'project_name')


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
