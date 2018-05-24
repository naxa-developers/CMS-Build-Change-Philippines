from django import forms
from .models import Project, Category, Material, Site, SiteMaterials, SiteDocument


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
        fields = ('name',)


class MaterialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Material
        exclude = ('project',)


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
