from django import forms
from django.contrib.auth.models import User
from .models import Project, Category, Material, Site, SiteMaterials, SiteDocument, ConstructionSteps, \
    ConstructionSubSteps, PrimaryPhoto, SubStepCheckList, BadPhoto, GoodPhoto
from django.forms.models import inlineformset_factory

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


class ConstructionSubStepsForm(forms.ModelForm):
    # primary_photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ConstructionSubSteps
        fields = ('title', 'title_de', 'description', 'description_de', 'order', 'call_inspector')


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

    construction_steps = forms.ModelMultipleChoiceField(
        queryset=ConstructionSteps.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = ConstructionSteps
        fields = ['construction_steps', ]


class SubStepCheckListForm(forms.ModelForm):

    class Meta:
        model = SubStepCheckList
        fields = ('text', 'description', 'step', 'substep')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['substep'].queryset = ConstructionSubSteps.objects.none()

        if 'step' in self.data:
            try:
                step_id = int(self.data.get('step'))
                self.fields['substep'].queryset = ConstructionSubSteps.objects.filter(step__site_steps=step_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['substep'].queryset = self.instance.step.sub_steps


PrimaryPhotoFormset = inlineformset_factory(ConstructionSubSteps, PrimaryPhoto, fields=['image', ], extra=1)
GoodPhotoFormset = inlineformset_factory(ConstructionSubSteps, GoodPhoto, fields=['image', ], extra=1)
BadPhotoFormset = inlineformset_factory(ConstructionSubSteps, BadPhoto, fields=['image', ], extra=1)





