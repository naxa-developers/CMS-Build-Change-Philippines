from django.contrib import admin

# Register your models here.
from userrole.models import UserRole
from core.models import Project, Site, Step
admin.site.register(UserRole)
admin.site.register(Project)
admin.site.register(Site)
admin.site.register(Step)