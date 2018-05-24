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
    location = PointField(srid=4326, null=True, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    name = models.CharField(max_length=250)
    site = models.ForeignKey(Site, related_name="steps", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, related_name="steps", on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_localname(self):
        try:
            if self.site.project.setting.local_language:
                return getattr(self, 'name_'+self.site.project.setting.local_language)
            else:
                return "No language chosen yet."
        except:
            return "No language chosen yet."


class Category(models.Model):
    name = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="category", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    title = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="material", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="material", on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True, null=True)
    good_photo = models.ImageField(upload_to="materials/good_photo", blank=True, null=True)
    bad_photo = models.ImageField(upload_to="materials/bad_photo", blank=True, null=True)
    
    def __str__(self):
        return self.title


class Checklist(models.Model):
    text = models.TextField(blank=True)
    step = models.ForeignKey(Step, related_name="checklist_steps", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name="checklist_material", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "step_id:" + str(self.step) + "------ id:" + str(self.id)

    def get_materials(self):
        if self.material_id:
            return reverse('core:material_update', kwargs={'pk': self.material_id})
        else:
            return None

    def get_localtext(self):
        try:
            if self.step.site.project.setting.local_language:
                return getattr(self, 'text_'+self.step.site.project.setting.local_language)
            else:
                return "No language chosen yet."
        except:
            return "No language chosen yet."


class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_report', on_delete=models.SET_NULL, null=True,
                             blank=True)
    checklist = models.ForeignKey(Checklist, related_name='checklist_report', on_delete=models.CASCADE)
    comment = models.TextField()
    photo = models.ImageField(upload_to='report/%Y/%m/%D/', null=True, blank=True)
    report_status = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now=True)


class CheckListHistroy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_checklist_history', on_delete=models.SET_NULL, null=True,
                             blank=True)
    checklist = models.ForeignKey(Checklist, related_name='checklist_history', on_delete=models.SET_NULL, null=True, blank=True)
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

