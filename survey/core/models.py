import os
from django.utils.timezone import datetime

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
from django.core.files.storage import FileSystemStorage
from django.db import transaction

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

LOG_ACTIONS = (
        ('phoned_to', 'phoned to'),
        ('submitted_a_response', 'submitted a response for general form'),
        ('updated_a_response', 'updated a response for general form'),
        # ('buy_object', 'User buy object'),
    )

PROJECT_TYPES = (
    (0, 'School'),
    (1, 'House'),
    (2, 'Others'),
)

REPORT_CATEGORY = [
    (0, 'Progress update'),
    (1, 'Issues/Concerns'),
    (2, 'Questions/Inquiries'),
]

REPORT_TYPE = [
    ('Urgent', 'Urgent'),
    ('Update', 'Update'),
    ('Alert', 'Alert'),
]


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


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


REPORT_STATUS = (
    ('0', 'Pending'),
    ('1', 'Responded'),
    ('2', 'Rejected'),
)


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
    good_photo = models.ImageField(verbose_name="Good Photo", upload_to="materials/good_photo", blank=True, null=True)
    bad_photo = models.ImageField(verbose_name="Bad Photo", upload_to="materials/bad_photo", blank=True, null=True)
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
    image = models.ImageField(upload_to='construction_step/', null=True, blank=True, storage=OverwriteStorage())
    project = models.ForeignKey(Project, related_name="construction_steps", on_delete=models.CASCADE, null=True,
                                blank=True)
    icon = models.ImageField(upload_to='construction_step/icons/', null=True, blank=True, storage=OverwriteStorage())

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
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    call_inspector = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # good,bad annd primary photo field not used
    good_photo = models.ImageField(upload_to="materials/good_photo", blank=True, null=True)
    bad_photo = models.ImageField(upload_to="materials/bad_photo", blank=True, null=True)
    primary_photo = models.ImageField(upload_to="materials/primary_photo", blank=True, null=True)

    def __str__(self):
        return self.title


class PrimaryPhoto(models.Model):
    construction_sub_step = models.ForeignKey(ConstructionSubSteps, related_name="primary_photos", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="materials/updated_primary_photo", blank=True, null=True, storage=OverwriteStorage())


class GoodPhoto(models.Model):
    construction_sub_step = models.ForeignKey(ConstructionSubSteps, related_name="good_photos", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="materials/updated_good_photo", blank=True, null=True, storage=OverwriteStorage())


class BadPhoto(models.Model):
    construction_sub_step = models.ForeignKey(ConstructionSubSteps, related_name="bad_photos", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="materials/updated_bad_photo", blank=True, null=True, storage=OverwriteStorage())


class SiteSteps(models.Model):
    site = models.ForeignKey(Site, related_name="site_steps", on_delete=models.CASCADE, null=True, blank=True)
    step = models.ForeignKey(ConstructionSteps, related_name="site_steps", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.step.name


class SubStepCheckList(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="checklists", null=True, blank=True)
    text = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True)
    step = models.ForeignKey(SiteSteps, related_name="checklists", on_delete=models.CASCADE)
    substep = models.ForeignKey(ConstructionSubSteps, related_name="checklists", on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{}-{}".format(self.text,self.substep)

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
    # def get_localtext(self):
    #     try:
    #         if self.step.site.project.setting.local_language:
    #             return getattr(self, 'text_' + self.step.site.project.setting.local_language)
    #         else:
    #             return "No Translation in Warray"
    #     except:
    #         return "No Translation in Warray"
    #
    # def get_status(self):
    #     return self.status


class NewCommonSubStepChecklist(models.Model):
    title = models.CharField(max_length=300)
    specification = models.TextField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="new_checklists", null=True, blank=True)
    substep = models.ForeignKey(ConstructionSubSteps, related_name="new_checklists", on_delete=models.CASCADE)
    step = models.ForeignKey(SiteSteps, related_name="new_checklists", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class NewSubStepChecklist(models.Model):
    common_checklist = models.ForeignKey(NewCommonSubStepChecklist, related_name="sub_checklists", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class ReportFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment', on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return self.feedback



REPORT_TYPE = [
    ('Urgent', 'Urgent'),
    ('Update', 'Update'),
    ('Alert', 'Alert'),
]


class SiteReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='site_reports', on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="site_reports", null=True, blank=True)
    comment = models.TextField()
    # photo = models.ImageField(upload_to='reports/', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=REPORT_STATUS, default=0)
    feedback = models.OneToOneField(ReportFeedback, related_name='site_feedback', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, choices=REPORT_TYPE, default=0)
    category = models.CharField(max_length=100, choices=REPORT_CATEGORY, default=0)


    def __str__(self):
        return self.comment

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         EventLog.objects.create(user=self.user, action='submitted_a_response', project_id=1, extra={'site':self.site.name, 'comment': self.comment})
    #     else:
    #         EventLog.objects.create(user=self.user, action='updated_a_response', project_id=1, extra={'site':self.site.name, 'comment': self.comment})

    #     super(SubstepReport, self).save(args, kwargs)


    class Meta:
        ordering = ('-date',)




class SubstepReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reports', on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    step = models.ForeignKey(SiteSteps, related_name="reports", on_delete=models.CASCADE, null=True, blank=True)
    substep = models.ForeignKey(ConstructionSubSteps, related_name='reports', on_delete=models.CASCADE)
    comment = models.TextField()
    # photo = models.ImageField(upload_to='reports/', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=REPORT_STATUS, default=0)
    feedback = models.OneToOneField(ReportFeedback, related_name='substep_feedback', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, choices=REPORT_CATEGORY, default=0)
    type = models.CharField(max_length=100, choices=REPORT_TYPE, default=0)


    def __str__(self):
        return self.comment

    def save(self, *args, **kwargs):
        super(SubstepReport, self).save(*args, **kwargs)
        for user in User.objects.all():
            notification = Notification()
            notification.report_id = self.id
            notification.user = user
            notification.read = False
            notification.save()

    class Meta:
        ordering = ('-date',)

class Images(models.Model):
    substepreport = models.ForeignKey(SubstepReport, on_delete=models.CASCADE, default=None)
    sitereport = models.ForeignKey(SiteReport, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='reports/', verbose_name='Image')


class Notification(models.Model):
    report = models.ForeignKey(SubstepReport, on_delete=models.CASCADE, related_name='notification')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification', on_delete=models.CASCADE, blank=True, null=True)
    read = models.BooleanField(default=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class HousesAndGeneralConstructionMaterials(models.Model):
    name = models.CharField(max_length=300)
    good_photo = models.ImageField(upload_to='HousesAndGeneralConstruction/materials/good_photo/', null=True, blank=True)
    good_photo_desc = models.TextField(null=True, blank=True)
    bad_photo = models.ImageField(upload_to='HousesAndGeneralConstruction/materials/bad_photo/', null=True, blank=True)
    bad_photo_desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name    


class BuildAHouseMakesHouseStrong(models.Model):
    name = models.CharField(max_length=300)
    pdf = models.FileField(upload_to='HousesAndGeneralConstruction/BuildAHouseMakesHouseStrong/pdf/', null=True, blank=True)

    def __str__(self):
        return self.name


class BuildAHouseKeyPartsOfHouse(models.Model):
    name = models.CharField(max_length=300)
    good_photo = models.ImageField(upload_to='HousesAndGeneralConstruction/KeyPartsOfHouse/good_photo/', null=True, blank=True)
    good_photo_desc = models.TextField(null=True, blank=True)
    bad_photo = models.ImageField(upload_to='HousesAndGeneralConstruction/KeyPartsOfHouse/bad_photo/', null=True, blank=True)
    bad_photo_desc = models.TextField(null=True, blank=True)    
    def __str__(self):
        return self.name


class StandardSchoolDesignPDF(models.Model):
    pdf = models.FileField(upload_to='HousesAndGeneralConstruction/', null=True, blank=True)
    


class CallLog(models.Model):
    call_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="call_to_log")
    call_from = models.ForeignKey(User, on_delete = models.CASCADE, related_name="call_from_log")
    time = models.DateTimeField(default=datetime.now)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         EventLog.objects.create(user=self.call_from, action='phoned_to', project_id=1, extra={'call_to':self.call_to.username})
    #     else:
    #         EventLog.objects.create(user=self.call_from, action='phoned_to', project_id=1, extra={'call_to':self.call_to.username})

    #     super(CallLog, self).save(args, kwargs)



class EventLog(models.Model):
    user = models.ForeignKey(User, related_name="event_logs", on_delete=models.CASCADE)
    action = models.CharField(max_length=300, choices=LOG_ACTIONS)
    project = models.ForeignKey(Project, related_name="event_logs", on_delete=models.CASCADE)
    extra = JSONField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.action