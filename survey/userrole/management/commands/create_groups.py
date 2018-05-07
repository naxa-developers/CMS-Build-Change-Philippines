from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        group_list = ['Project Manager', 'Field Engineer', 'Community Member', 'Super Admin']
        for group in group_list:
            new_group, created = Group.objects.get_or_create(name=group)

            if created:
                self.stdout.write('Successfully created group .. "%s"' % new_group)