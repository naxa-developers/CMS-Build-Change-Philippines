from modeltranslation.translator import register, TranslationOptions
from .models import Step, Checklist

@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Checklist)
class ChecklistTranslationOptions(TranslationOptions):
    fields = ('text',)

