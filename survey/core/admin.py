from django.contrib import admin

# Register your models here.
from core.models import Project, Report, SiteDocument, ConstructionSteps, SiteSteps
admin.site.register(Report)
admin.site.register(SiteDocument)
admin.site.register(ConstructionSteps)
admin.site.register(SiteSteps)
