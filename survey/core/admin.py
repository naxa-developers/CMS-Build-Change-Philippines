from django.contrib import admin

# Register your models here.
from core.models import Project, Report, SiteDocument
admin.site.register(Report)
admin.site.register(SiteDocument)

