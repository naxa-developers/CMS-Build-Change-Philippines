from django.core.management.base import BaseCommand

from core.models import ConstructionStepsTitle


class Command(BaseCommand):
    help = 'Create default construction_steps'

    def handle(self, *args, **options):

        CONSTRUCTION_STEPS_LIST = \
            ["Construction Of Ring Beams",
             "Construction Of Lintel Beams On The Openings",
             "Electrical Works",
             "Installation Of Ceiling",
             "Paint Works",

             ]
        for construction_step in CONSTRUCTION_STEPS_LIST:
            new_construction_step, created = ConstructionStepsTitle.objects.get_or_create(title=construction_step)
            if created:
                self.stdout.write('Successfully created construction_step .. "%s"' % construction_step)
