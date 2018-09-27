from django.contrib import admin

# Register your models here.
from core.models import Project, Report, SiteDocument, ConstructionSubSteps, ConstructionSteps, SiteSteps, PrimaryPhoto, SubStepCheckList, GoodPhoto, BadPhoto
from userrole.models import FieldEngineerProfile


class PrimaryPhotoInline(admin.StackedInline):
    model = PrimaryPhoto
    extra = 1


class GoodPhotoInline(admin.StackedInline):
    model = GoodPhoto
    extra = 1


class BadPhotoInline(admin.StackedInline):
    model = BadPhoto
    extra = 1


class ConstructionSubStepsAdmin(admin.ModelAdmin):
    inlines = (PrimaryPhotoInline, GoodPhotoInline, BadPhotoInline)


admin.site.register(Report)
admin.site.register(SiteDocument)
admin.site.register(ConstructionSteps)
admin.site.register(ConstructionSubSteps, ConstructionSubStepsAdmin)
admin.site.register(SiteSteps)
admin.site.register(SubStepCheckList)