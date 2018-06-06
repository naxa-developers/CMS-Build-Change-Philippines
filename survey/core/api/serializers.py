from rest_framework import serializers
from core.models import Project, Site, Step, Checklist, Material, Report, Category, SiteMaterials, SiteDocument


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
    category = serializers.CharField(source='category.name')
    local_category = serializers.CharField(source='category.get_localname')

    class Meta:
        model = Material
        fields = ('id', 'title', 'description', 'good_photo', 'bad_photo', 'project', 'category', 'local_category')


class StepSerializer(serializers.ModelSerializer):
    localname = serializers.ReadOnlyField(source="get_localname")

    class Meta:
        model = Step
        fields = ('id','name', 'site', 'project', 'order','localname')

    def create(self, validated_data):
        localname = validated_data.pop('localname') if 'localname' in validated_data else ""
        instance = super(StepSerializer, self).create(validated_data)
        instance.created_by = self.context['request'].user
        project = instance.site.project
        setattr(instance, 'name_'+project.setting.local_language, localname)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        localname = self.context['request'].data.get('localname', "")
        instance =  super(StepSerializer, self).update(instance, validated_data)
        project = instance.site.project
        setattr(instance, 'name_' + project.setting.local_language, localname)
        instance.save()
        return instance


class ChecklistSerializer(serializers.ModelSerializer):
    localtext = serializers.ReadOnlyField(source="get_localtext")
    materials = serializers.SerializerMethodField()
    last_submission = serializers.SerializerMethodField()

    class Meta:
        model = Checklist
        fields = ('id', 'text', 'step', 'localtext', 'materials','material', 'last_submission')

    def get_materials(self, obj):
        if obj.material:
            serializer = MaterialSerializer(instance=obj.material, many=False)
            return serializer.data
        return {}

    def get_last_submission(self, obj):
        return {}

    def create(self, validated_data):
        localname = validated_data.pop('localtext') if 'localtext' in validated_data else ""
        instance = super(ChecklistSerializer, self).create(validated_data)
        project = instance.step.site.project
        if project.setting.local_language:
            setattr(instance, 'text_'+project.setting.local_language, localname)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        localname = self.context['request'].data.get('localtext', "")
        instance = super(ChecklistSerializer, self).update(instance, validated_data)
        project = instance.step.site.project
        setattr(instance, 'text_' + project.setting.local_language, localname)
        instance.save()
        return instance


class StepDetailSerializer(serializers.ModelSerializer):
    localname = serializers.ReadOnlyField(source="get_localname")
    checklists = serializers.SerializerMethodField()

    class Meta:
        model = Step
        fields = ('id','name', 'site', 'project', 'order','localname', 'checklists')

    def get_checklists(self, obj):
        qs = obj.checklist_steps.all()
        return  ChecklistSerializer(qs, many=True).data


class SitesSerializer(serializers.ModelSerializer):
    steps = StepDetailSerializer(many=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'address', 'steps')


class ProjectSerializer(serializers.ModelSerializer):
    sites = SitesSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'sites')


class ReportSerializer(serializers.ModelSerializer):
    step_id = serializers.IntegerField(source='checklist.step.id', read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'user', 'step_id', 'checklist', 'comment', 'photo', 'report_status', 'date')


class CategorySerializer(serializers.ModelSerializer):
    localname = serializers.ReadOnlyField(source="get_localname")
    project_name = serializers.CharField(source='project.name')

    class Meta:
        model = Category
        fields = ('id', 'name', 'localname', 'project', 'project_name')

    def create(self, validated_data):
        localname = validated_data.pop('localname') if 'localname' in validated_data else ""
        instance = super(CategorySerializer, self).create(validated_data)
        project = instance.project
        setattr(instance, 'name_' + project.setting.local_language, localname)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        localname = self.context['request'].data.get('localname', "")
        instance = super(CategorySerializer, self).update(instance, validated_data)
        project = instance.project
        setattr(instance, 'name_' + project.setting.local_language, localname)
        instance.save()
        return instance


class SiteMaterialSerializer(serializers.ModelSerializer):
    site = serializers.CharField(source='site.name')
    materials = MaterialSerializer(many=True)

    class Meta:
        model = SiteMaterials
        fields = ('id', 'site', 'materials')


class SiteDocumentSerializer(serializers.ModelSerializer):
    site = serializers.CharField(source='site.name')

    class Meta:
        model = SiteDocument
        fields = ('id', 'site', 'file', 'document_name')
