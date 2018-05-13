from modeltranslation.translator import register, TranslationOptions
from .models import Step

@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('name',)

