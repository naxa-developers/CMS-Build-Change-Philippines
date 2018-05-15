from django.contrib import admin

from userrole.models import UserRole
from core.models import Project, Site, Step, Category, Material, Checklist, Setting

# Register your models here.


class MyModelAdmin(admin.ModelAdmin):
    model = Material

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Material.objects.filter(project=request.object.project.pk)
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(UserRole)
admin.site.register(Project)
admin.site.register(Site)
admin.site.register(Step)
admin.site.register(Checklist)
admin.site.register(Setting)
admin.site.register(Category)
admin.site.register(Material, MyModelAdmin)
