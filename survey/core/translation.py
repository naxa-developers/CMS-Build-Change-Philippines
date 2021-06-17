from modeltranslation.translator import register, TranslationOptions
from .models import Step, Checklist, Material, Category, ConstructionSteps, ConstructionSubSteps, HousesAndGeneralConstructionMaterials, BuildAHouseMakesHouseStrong, BuildAHouseKeyPartsOfHouse


@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Checklist)
class ChecklistTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Material)
class ChecklistTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ConstructionSteps)
class ConstructionStepsTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ConstructionSubSteps)
class ConstructionStepsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(HousesAndGeneralConstructionMaterials)
class HousesAndGeneralConstructionMaterialsTranslationOptions(TranslationOptions):
    fields = ('name', 'good_photo_desc', 'bad_photo_desc')


@register(BuildAHouseMakesHouseStrong)
class BuildAHouseMakesHouseStrongTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(BuildAHouseKeyPartsOfHouse)
class BuildAHouseKeyPartsOfHouseTranslationOptions(TranslationOptions):
    fields = ('name', 'good_photo_desc', 'bad_photo_desc')
