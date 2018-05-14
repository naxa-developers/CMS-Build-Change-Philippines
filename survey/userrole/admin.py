from django.contrib import admin

# Register your models here.
from userrole.models import UserRole
from core.models import Project, Site, Step, Checklist, Setting
admin.site.register(UserRole)
admin.site.register(Project)
admin.site.register(Site)
admin.site.register(Step)
admin.site.register(Checklist)
admin.site.register(Setting)