from django.contrib import admin

# Register your models here.
from core.models import Project, Report, SiteDocument, ConstructionSubSteps, ConstructionSteps, SiteSteps
from userrole.models import FieldEngineerProfile


admin.site.register(Report)
admin.site.register(SiteDocument)
admin.site.register(ConstructionSteps)
admin.site.register(ConstructionSubSteps)
admin.site.register(SiteSteps)
# admin.site.register(FieldEngineerProfile)