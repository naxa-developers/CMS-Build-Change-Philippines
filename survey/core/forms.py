from django import forms

from .models import Project, Category, Material
from modeltranslation.forms import TranslationModelForm


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name',  'organization', 'logo', 'type', 'address',
                  'phone_number', 'email_address', 'short_description')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)


class MaterialForm(TranslationModelForm):

    class Meta:
        model = Material
        exclude = ()
