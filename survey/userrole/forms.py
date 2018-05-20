from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserRole


class UserRoleForm(forms.ModelForm):

    class Meta:
        model = UserRole
        fields = ('user',)


class UserProfileForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

