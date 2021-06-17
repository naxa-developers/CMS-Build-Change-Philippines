from django.core.management.base import BaseCommand

from core.models import HousesAndGeneralConstructionMaterials


class Command(BaseCommand):
    help = 'Create default HousesAndGeneralConstructionMaterials'

    def handle(self, *args, **options):

        Houses_and_general_construction_materials = \
            ["CEMENT",
             "SAND",
             "GRAVEL",
             "HOLLOW BLOCKS",
             "STEEL BARS",
             "WOOD",

             ]
        for materials in Houses_and_general_construction_materials:
            materials, created = HousesAndGeneralConstructionMaterials.objects.get_or_create(name=materials)
            if created:
                self.stdout.write('Successfully created materials .. "%s"' % materials)
