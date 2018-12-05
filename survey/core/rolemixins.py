from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Project, Site


class ProjectView(LoginRequiredMixin):

    def form_valid(self, form):
        if self.request.project:
            form.instance.project = self.request.project
        return super(ProjectView, self).form_valid(form)

    def get_queryset(self):
        if self.request.project:
            return super(ProjectView, self).get_queryset().filter(project=self.request.project)
        else:
            return super(ProjectView, self).get_queryset()

    def get_form(self, *args, **kwargs):
        form = super(ProjectView, self).get_form(*args, **kwargs)
        if self.request.project:
            form.project = self.request.project
        if hasattr(form.Meta, 'project_filters'):
            for field in form.Meta.project_filters:
                if self.request.project:
                    form.fields[field].queryset = Project.objects.filter(id=self.request.project.pk)
                elif self.request.organization:
                    form.fields[field].queryset = Project.objects.filter(organization=self.request.organization)
        return form


class ProjectRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(ProjectRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            project_id = self.kwargs.get('pk')
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(ProjectRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('project_id'):
            project_id = self.kwargs.get('project_id')
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(ProjectRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class SiteRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(SiteRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            project_id = get_object_or_404(Project, sites=self.kwargs.get('pk'))
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(SiteRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('project_id'):
            project_id = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(SiteRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class CategoryRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(CategoryRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            category_id = self.kwargs.get('pk')
            project_id = get_object_or_404(Project, category=category_id)
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(CategoryRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('project_id'):
            project_id = self.kwargs.get('project_id')
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(CategoryRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class ProjectGuidelineRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(ProjectGuidelineRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            material_id = self.kwargs.get('pk')
            project_id = get_object_or_404(Project, material=material_id)
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(ProjectGuidelineRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('project_id'):
            project_id = self.kwargs.get('project_id')
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(ProjectGuidelineRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class SiteGuidelineRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(SiteGuidelineRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('site_id'):
            project_id = get_object_or_404(Project, sites=self.kwargs.get('site_id'))
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(SiteGuidelineRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            site_id = Site.objects.get(site_site_materials=self.kwargs.get('pk'))
            project_id = get_object_or_404(Project, sites=site_id)
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(SiteGuidelineRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class DocumentRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(DocumentRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('site_id'):
            project_id = get_object_or_404(Project, sites=self.kwargs.get('site_id'))
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(DocumentRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            site_id = Site.objects.get(site_document=self.kwargs.get('pk'))
            project_id = get_object_or_404(Project, sites=site_id)
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(DocumentRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class ReportRoleMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.group.name == "Super Admin":
            return super(ReportRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('site_pk'):
            project_id = get_object_or_404(Project, sites=self.kwargs.get('site_pk'))
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(ReportRoleMixin, self).dispatch(request, *args, **kwargs)

        elif self.kwargs.get('pk'):
            site_id = Site.objects.get(steps__checklist_steps__checklist_report=self.kwargs.get('pk'))
            project_id = get_object_or_404(Project, sites=site_id)
            user_id = request.user.id
            user_role = request.roles.filter(user_id=user_id, project_id=project_id, group__name="Project Manager")

            if user_role:
                return super(ReportRoleMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied()