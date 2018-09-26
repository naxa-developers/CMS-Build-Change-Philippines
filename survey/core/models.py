import os
from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db.models import PointField

from rest_framework.authtoken.models import Token


PROJECT_TYPES = (
    (0, 'School'),
    (1, 'House'),
    (2, 'Others'),
)


class Project(models.Model):
    name = models.CharField(max_length=250)
    organization = models.CharField(max_length=250, null=True, blank=True)
    logo = models.ImageField(upload_to="project/logo/", null=True, blank=True)
    type = models.IntegerField(choices=PROJECT_TYPES, default=0)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email_address = models.EmailField(max_length=250, null=True, blank=True)
    short_description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    def total_sites(self):
        return self.sites.count()

    def total_reports(self):
        return self.steps.values('checklist_steps__checklist_report').count()

    def total_personnel(self):
        project_manager = self.project_roles.filter(group__name="Project Manager").count()
        field_engineer = self.project_roles.filter(group__name="Field Engineer").count()
        community_member = self.project_roles.filter(group__name="Community Member").count()
        return project_manager + field_engineer + community_member

    def total_common_users(self):
        return self.project_roles.filter(group__name="Community Member").count()


class Setting(models.Model):
    local_language = models.CharField(choices=settings.LANGUAGES, max_length=2, null=True, blank=True)
    site_display = models.CharField(max_length=250, null=True, blank=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, blank=True, null=True)


SITE_TYPES = (
    (0, 'Type I'),
    (1, 'Type II'),
    (2, 'Type III'),
)


class Site(models.Model):
    name = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="sites", on_delete=models.CASCADE)
    type = models.IntegerField(choices=SITE_TYPES, default=0)
    photo = models.ImageField(upload_to="site/photo/", null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    location = PointField(null=True, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_latitude(self):
        return self.location.y

    @property
    def get_longitude(self):
        return self.location.x


class Step(models.Model):
    name = models.CharField(max_length=250)
    site = models.ForeignKey(Site, related_name="steps", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, related_name="steps", on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField()
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_localname(self):
        try:
            if self.site.project.setting.local_language:
                return getattr(self, 'name_' + self.site.project.setting.local_language)
            else:
                return "No Translation in Warray"
        except:
            return "No Translation in Warray"


class Category(models.Model):
    name = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="category", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_localname(self):
        try:
            if self.project.setting.local_language:
                return getattr(self, 'name_' + self.project.setting.local_language)
            else:
                return "No Translation in Warray"
        except:
            return "No Translation in Warray"

    @property
    def materials(self):
        return self.material


class Material(models.Model):
    title = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="material", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="material", on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True, null=True)
    good_photo = models.ImageField(upload_to="materials/good_photo", blank=True, null=True)
    bad_photo = models.ImageField(upload_to="materials/bad_photo", blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Checklist(models.Model):
    text = models.TextField(blank=True)
    step = models.ForeignKey(Step, related_name="checklist_steps", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name="checklist_material", null=True, blank=True,
                                 on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)

    @property
    def step_checklist(self):
        return "step_id:" + str(self.step) + "------ id:" + str(self.id)

    def get_materials(self):
        if self.material_id:
            return reverse('core:material_update', kwargs={'pk': self.material_id})
        else:
            return None

    def get_localtext(self):
        try:
            if self.step.site.project.setting.local_language:
                return getattr(self, 'text_' + self.step.site.project.setting.local_language)
            else:
                return "No Translation in Warray"
        except:
            return "No Translation in Warray"

    def get_status(self):
        return self.status


class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_report', on_delete=models.SET_NULL, null=True,
                             blank=True)
    checklist = models.ForeignKey(Checklist, related_name='checklist_report', on_delete=models.CASCADE)
    comment = models.TextField()
    photo = models.ImageField(upload_to='report/', null=True, blank=True)
    report_status = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('-date',)


class CheckListHistroy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_checklist_history', on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    checklist = models.ForeignKey(Checklist, related_name='checklist_history', on_delete=models.SET_NULL, null=True,
                                  blank=True)
    old_status = models.BooleanField()
    new_status = models.BooleanField()
    date = models.DateTimeField(auto_now=True)


class SiteMaterials(models.Model):
    site = models.ForeignKey(Site, related_name='site_site_materials', on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, related_name='site_materials')


class SiteDocument(models.Model):
    site = models.ForeignKey(Site, related_name="site_document", on_delete=models.CASCADE)
    file = models.FileField(upload_to='site/documents')
    document_name = models.CharField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):

        # print(os.system('chmod 777 -R media/site/documents/Personnell_Utilization_Share.xlsx'))
        # print(os.path.basename(self.file.url))
        # os.system('chmod 777 -R media/site/documents/' + str(self.file.name))
        # os.system('chmod 777 -R media/site/documents/' + self.file.name)
        # print(os.path.join(settings.BASE_DIR, "media"))
        # print('chmod 777 -R ' + path + self.file.name)
        # os.system('chmod 777 -R ' + path + self.file.name)

        super().save(*args, **kwargs)

    def get_name(self):
        base = os.path.basename(self.file.path)
        return os.path.splitext(base)[0]

    def css_class(self):
        name, extension = os.path.splitext(self.file.path)
        if extension == '.pdf':
            return 'pdf'
        if extension == '.doc' or extension == '.docx':
            return 'word'
        if extension == '.xlsx':
            return 'excel'
        if extension == '.ppt':
            return 'powerpoint'
        if extension == '.png' or extension == '.jpg' or extension == '.jpeg':
            return 'image'
        if extension == '.zip':
            return 'zip'
        return 'pdf'


# Updated models

CONSTRUCTION_STEPS_LIST = \
    ["Construction Of Ring Beams",
     "Construction Of Lintel Beams On The Openings",
     "Electrical Works",
     "Installation Of Ceiling",
     "Paint Works",

     ]

CONSTRUCTION_SUB_STEPS_LIST = [
            {"Construction Of Ring Beams": ["Chipping Of Walls", "Rebar Works", "Installation Of Form Works", "Concrete Works",
                                            "Removal Of Form Works"]},
            {"Construction Of Lintel Beams On The Openings": ["Chipping Of Walls", "Rebar Works", "Installation Of Form Works", "Concrete Works",
                                            "Removal Of Form Works"]},
            {"Electrical Works": ["Layout Of Wirings", "Installation Of Electrical Fixtures"]},
            {"Installation Of Ceiling": ["Installation Of Ceiling Joist"]},


        ]


class ConstructionSteps(models.Model):
    name = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="construction_steps", on_delete=models.CASCADE, null=True,
                                blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_localname(self):
        try:
            if self.project.setting.local_language:
                return getattr(self, 'name_' + self.project.setting.local_language)
            else:
                return "No Translation in Warray"
        except:
            return "No Translation in Warray"


class ConstructionSubSteps(models.Model):
    title = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="construction_substeps", on_delete=models.CASCADE, null=True, blank=True)
    step = models.ForeignKey(ConstructionSteps, related_name="sub_steps", on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True, null=True)
    good_photo = models.ImageField(upload_to="materials/good_photo", blank=True, null=True)
    bad_photo = models.ImageField(upload_to="materials/bad_photo", blank=True, null=True)
    primary_photo = models.ImageField(upload_to="materials/primary_photo", blank=True, null=True)
    order = models.IntegerField(default=0)
    call_inspector = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PrimaryPhoto(models.Model):
    construction_sub_step = models.ForeignKey(ConstructionSubSteps, related_name="primary_photos", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="materials/updated_primary_photo", blank=True, null=True)


class SiteSteps(models.Model):
    site = models.ForeignKey(Site, related_name="site_steps", on_delete=models.CASCADE, null=True, blank=True)
    step = models.ForeignKey(ConstructionSteps, related_name="site_steps", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.step.name


class SubStepCheckList(models.Model):
    text = models.TextField(blank=True)
    step = models.ForeignKey(ConstructionSteps, related_name="checklists", on_delete=models.CASCADE)
    substep = models.ForeignKey(ConstructionSubSteps, related_name="checklists", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)

    # @property
    # def step_checklist(self):
    #     return "step_id:" + str(self.step) + "------ id:" + str(self.id)
    #
    # def get_materials(self):
    #     if self.material_id:
    #         return reverse('core:material_update', kwargs={'pk': self.material_id})
    #     else:
    #         return None
    #
    def get_localtext(self):
        try:
            if self.step.site.project.setting.local_language:
                return getattr(self, 'text_' + self.step.site.project.setting.local_language)
            else:
                return "No Translation in Warray"
        except:
            return "No Translation in Warray"

    # def get_status(self):
    #     return self.status


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
