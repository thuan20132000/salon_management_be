from django.core.management.base import BaseCommand
from salon.models import NailServiceCategory


class Command(BaseCommand):
    help = 'Seed NailServiceCategory data'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Pedicure & Manicure', 'description': 'Pedicure & Manicure services'},
            {'name': 'Kid Service', 'description': 'Kid services'},
            {'name': 'Nail Extensions', 'description': 'Nail Extensions services'},
            {'name': 'Extra Services', 'description': 'Extra services'},
            {'name': 'Waxing', 'description': 'Waxing services'},
            {'name': 'Eyebrow Tinting', 'description': 'Eyebrow Tinting services'},
            {'name': 'Block Time', 'description': 'Block Time services'},
        ]

        for category_data in categories:
            category, created = NailServiceCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully added {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'{category.name} already exists'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully seeded NailServiceCategory data'))
