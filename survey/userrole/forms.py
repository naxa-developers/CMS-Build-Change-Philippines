from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string

from survey import settings
from .models import UserRole, Project
from django.core.mail import EmailMultiAlternatives

class UserRoleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = None

        for field in iter(self.fields):

            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

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

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProjectUserForm(UserCreationForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })


class SendInvitationForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    def send_email(self):
        subject, from_email, to = 'Invitation Testing', settings.EMAIL_HOST_USER, self.cleaned_data['email']
        html_content = '<html><body><p>CMS Builders Invitation.</p><br>Sign Up<a href="http://bccms.naxa.com.np/userrole/project-user-create/2/"><h2>here</h2></a></body></html>'
        email = EmailMultiAlternatives(subject, body='This is an Invitation Email from CMS Builders. Testing!',\
                                       from_email=from_email, to=[to])
        email.attach_alternative(html_content, "text/html")
        try:
            # email.send()
            return email.send(fail_silently=False)
        except:
            return HttpResponse('Invalid header found.')
