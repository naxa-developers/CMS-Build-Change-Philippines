from django.core.management.base import BaseCommand

from core.models import BuildAHouseMakesHouseStrong


class Command(BaseCommand):
    help = 'Create default BuildAHouseMakesHouseStrong'

    def handle(self, *args, **options):

        BuildAHouse_makes_house_strong = \
            ["CONFIGURATION",
             "CONNECTION",
             "CONSTRUCTION QUALITY",

             ]
        for strong_house in BuildAHouse_makes_house_strong:
            strong_house, created = BuildAHouseMakesHouseStrong.objects.get_or_create(name=strong_house)
            if created:
                self.stdout.write('Successfully created strong_house .. "%s"' % strong_house)
