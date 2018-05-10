from django.db import models
from django.contrib.postgres.fields import JSONField

from phonenumber_field.modelfields import PhoneNumberField

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
    sites = models.ForeignKey(Site, related_name="steps", on_delete=models.CASCADE)
    order = models.IntegerField()
    checklist = JSONField()

    def project(self):
        return self.sites.project.id

    def __str__(self):
        return self.name
