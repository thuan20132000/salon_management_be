from django.core.management.base import BaseCommand
from salon.models import UserLevel

class Command(BaseCommand):
    help = 'Seed UserLevel data'

    def handle(self, *args, **kwargs):
        levels = [
            'Junior',
            'Intermediate',
            'Senior',
            'Manager',
            'Owner'
        ]

        for level in levels:
            UserLevel.objects.get_or_create(name=level)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {level} level'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded UserLevel data'))