from modeltranslation.translator import register, TranslationOptions
from .models import Step, Checklist, Material, Category, ConstructionSteps, ConstructionSubSteps


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

