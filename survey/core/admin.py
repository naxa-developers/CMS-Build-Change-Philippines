from django.contrib import admin
from import_export import resources

# Register your models here.
from core.models import Project, Report, SiteDocument, ConstructionSubSteps, ConstructionSteps, SiteSteps, PrimaryPhoto, SubStepCheckList, GoodPhoto, BadPhoto, HousesAndGeneralConstructionMaterials, BuildAHouseKeyPartsOfHouse, BuildAHouseMakesHouseStrong, StandardSchoolDesignPDF, EventLog, CallLog, SubstepReport, NewSubStepChecklist, NewCommonSubStepChecklist, SiteReport, Images
from userrole.models import FieldEngineerProfile, AdminProfile


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


class StandardSchoolDesignPDFAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return StandardSchoolDesignPDF.objects.all().count() == 0


admin.site.register(SiteDocument)
admin.site.register(ConstructionSteps)
admin.site.register(ConstructionSubSteps, ConstructionSubStepsAdmin)
admin.site.register(SiteSteps)
admin.site.register(SubStepCheckList)
admin.site.register(HousesAndGeneralConstructionMaterials)
admin.site.register(BuildAHouseMakesHouseStrong)
admin.site.register(BuildAHouseKeyPartsOfHouse)
admin.site.register(StandardSchoolDesignPDF, StandardSchoolDesignPDFAdmin)
# admin.site.register(AdminProfile)
admin.site.register(EventLog)
admin.site.register(CallLog)
admin.site.register(SubstepReport)
admin.site.register(SiteReport)
admin.site.register(NewCommonSubStepChecklist)
admin.site.register(NewSubStepChecklist)
admin.site.register(Images)


class SubStepCheckListResource(resources.ModelResource):

    class Meta:
        model = SubStepCheckList
        fields = ('id', 'text', 'status',)
