from django.db import models
from django.contrib.postgres.fields import JSONField


class Project(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=250)
    project = models.ForeignKey(Project, related_name="sites", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Step(models.Model):
    name = models.CharField(max_length=250)
    sites = models.ForeignKey(Site, related_name="steps", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, related_name="steps", on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField()
    checklist = JSONField()

    def project(self):
        return self.sites.project.id

    def __str__(self):
        return self.name
