from django.core.management.base import BaseCommand

from core.models import BuildAHouseKeyPartsOfHouse


class Command(BaseCommand):
    help = 'Create default BuildAHouseKeyPartsOfHouse'

    def handle(self, *args, **options):

        Build_a_house_key_parts_of_house = \
            ["FOUNDATION",
             "FLOOR SLAB",
             "COLUMN",
             "WALLS",
             "BEAMS",
             "ROOF",

             ]
        for keyparts in Build_a_house_key_parts_of_house:
            keyparts, created = BuildAHouseKeyPartsOfHouse.objects.get_or_create(name=keyparts)
            if created:
                self.stdout.write('Successfully created keyparts .. "%s"' % keyparts)
