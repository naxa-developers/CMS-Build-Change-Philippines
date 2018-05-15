from django.db import models
from django.contrib.postgres.fields import JSONField

from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

PROJECT_TYPES = (
    (0, 'First Type'),
    (1, 'Second Type'),
    (2, 'Third Type'),
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
    (0, 'First Type'),
    (1, 'Second Type'),
    (2, 'Third Type'),
)


class Site(models.Model):
    name = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="sites", on_delete=models.CASCADE)
    type = models.IntegerField(choices=SITE_TYPES, default=0)
    photo = models.ImageField(upload_to="site/photo/", null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.name

class Step(models.Model):
    name = models.CharField(max_length=250)
    site = models.ForeignKey(Site, related_name="steps", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, related_name="steps", on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField()
    

    def __str__(self):
        return self.name

    def get_localname(self):
        try:
            if self.project.setting.local_language:
                return getattr(self, 'name_'+self.project.setting.local_language)
            else:
                return "No language chosen yet."
        except:
            return "No language chosen yet."



class Checklist(models.Model):
    text = models.TextField(blank=True)
    step = models.ForeignKey(Step, related_name="checklist_steps", on_delete=models.CASCADE)
    

    def __str__(self):
        return "step_id:" + str(self.step) + "------ id:" + str(self.id)

    def get_localtext(self):
        try:
            if self.step.project.setting.local_language:
                return getattr(self, 'text_'+self.step.project.setting.local_language)
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
    description = models.TextField(max_length=300)
    good_photo = models.ImageField(upload_to="material/good_photo/%Y/%m/%D/")
    bad_photo = models.ImageField(upload_to="material/bad_photo/%Y/%m/%D/")
    checklist = models.ForeignKey(Checklist, related_name="checklist_material", null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

