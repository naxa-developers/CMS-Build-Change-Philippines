from modeltranslation.translator import register, TranslationOptions
from .models import Step, Checklist

@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('name',)

class StepTranslationOptions(TranslationOptions):
    fields = ('text',)

