from django import forms
from django.contrib.auth.models import User
from .models import Project, Category, Material, Site, SiteMaterials, SiteDocument, ConstructionSteps

from mapwidgets.widgets import GooglePointFieldWidget


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Project
        fields = ('name',  'organization', 'logo', 'type', 'address',
                  'phone_number', 'email_address', 'short_description')


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Category
        exclude = ('project', 'name_en')


class MaterialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Material
        exclude = ('project', 'title_en', 'description_en', 'created_by')


class SiteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Site
        exclude = ('project',)
        widgets = {
            'location': GooglePointFieldWidget,
        }


class SiteMaterialsForm(forms.ModelForm):

    class Meta:
        model = SiteMaterials
        fields = ('materials',)

        widgets = {
            'materials': forms.CheckboxSelectMultiple()
        }


class SiteDocumentForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = SiteDocument
        fields = ('file', 'document_name')


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# Updated form
class SiteConstructionStepsForm(forms.ModelForm):
    """ Form to create prakop, baali, mausam, prakop starikaran list for project """

    construction_steps = forms.ModelMultipleChoiceField(
        queryset=ConstructionSteps.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = ConstructionSteps
        fields = ['construction_steps',]


