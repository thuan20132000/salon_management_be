from django.core.management.base import BaseCommand
from salon.models import NailServiceCategory, NailService
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed NailService data'

    def handle(self, *args, **kwargs):
        services = [
            {'name': 'Basic Pedicure', 'description': 'Basic Pedicure service',
                'category': 'Pedicure & Manicure', 'price': 25.00, 'duration': 35},
            {'name': 'Basic Manicure', 'description': 'Basic Manicure service',
                'category': 'Pedicure & Manicure', 'price': 20.00, 'duration': 23},
            {'name': 'Kid Pedicure', 'description': 'Pedicure service for kids',
                'category': 'Kid Service', 'price': 15.00, 'duration': 35},
            {'name': 'Kid Manicure', 'description': 'Manicure service for kids',
                'category': 'Kid Service', 'price': 10.00, 'duration': 35},
            {'name': 'Acrylic Full Set', 'description': 'Acrylic nail extensions full set',
                'category': 'Nail Extensions', 'price': 40.00, 'duration': 35},
            {'name': 'Gel Full Set', 'description': 'Gel nail extensions full set',
                'category': 'Nail Extensions', 'price': 35.00, 'duration': 35},
            {'name': 'Paraffin Wax', 'description': 'Paraffin wax treatment',
                'category': 'Extra Services', 'price': 15.00, 'duration': 35},
            {'name': 'Eyebrow Waxing', 'description': 'Eyebrow waxing service',
                'category': 'Waxing', 'price': 10.00, 'duration': 35},
            {'name': 'Eyebrow Tint', 'description': 'Eyebrow tinting service',
                'category': 'Eyebrow Tinting', 'price': 12.00, 'duration': 35},
            {'name': '30 Minute Block', 'description': '30 minutes of service time',
                'category': 'Block Time', 'price': 30.00, 'duration': 35},
        ]

        for service_data in services:
            category_name = service_data.pop('category')
            category = NailServiceCategory.objects.get(name=category_name)
            service, created = NailService.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'category': category,
                    'price': service_data['price'],
                    'duration': service_data['duration']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully added {service.name}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'{service.name} already exists'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully seeded NailService data'))
