from django import template
from django.db import models
register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.user_roles.values(name=models.F('group__name')).filter(name=group_name).exists()