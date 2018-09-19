from django.core.management.base import BaseCommand

from core.models import ConstructionSteps


class Command(BaseCommand):
    help = 'Create default construction_steps'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)

    def handle(self, *args, **options):
        project_id = options['project_id']

        CONSTRUCTION_STEPS_LIST = \
            ["Construction Of Ring Beams",
             "Construction Of Lintel Beams On The Openings",
             "Electrical Works",
             "Installation Of Ceiling",
             "Paint Works",

             ]
        for construction_step in CONSTRUCTION_STEPS_LIST:
            new_construction_step, created = ConstructionSteps.objects.get_or_create(title=construction_step, project_id=project_id)
            if created:
                self.stdout.write('Successfully created construction_step .. "%s"' % construction_step)
