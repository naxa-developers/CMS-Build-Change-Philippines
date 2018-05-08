from django import forms

from .models import UserRole


class UserRoleForm(forms.ModelForm):

    class Meta:
        model = UserRole
        fields = ('user',)