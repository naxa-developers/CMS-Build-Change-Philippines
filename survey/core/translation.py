from modeltranslation.translator import register, TranslationOptions
from .models import Step, Checklist, Material

@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Checklist)
class ChecklistTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(Material)
class ChecklistTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

