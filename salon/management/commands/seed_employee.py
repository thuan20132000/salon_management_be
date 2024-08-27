from django.core.management.base import BaseCommand
from salon.models import Employee, UserLevel
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed Employee data'

    def handle(self, *args, **kwargs):
        # Ensure UserLevels exist
        levels = ['Junior', 'Intermediate', 'Senior', 'Manager', 'Owner']
        for level in levels:
            UserLevel.objects.get_or_create(name=level)

        # Seed Employee data
        employees = [
            {
                'username': 'john_doe',
                'phone_number': '1234567890',
                'level': 'Junior',
                'start_date': timezone.now().date(),
                'job_title': 'Nail Technician',
                'birth_date': '1990-01-01',
                'insurance_number': 'INS123456'
            },
            {
                'username': 'jane_smith',
                'phone_number': '0987654321',
                'level': 'Senior',
                'start_date': timezone.now().date(),
                'job_title': 'Senior Nail Technician',
                'birth_date': '1985-05-15',
                'insurance_number': 'INS654321'
            }
        ]

        for emp_data in employees:
            level = UserLevel.objects.get(name=emp_data['level'])
            emp, created = Employee.objects.get_or_create(
                username=emp_data['username'],
                defaults={
                    'phone_number': emp_data['phone_number'],
                    'level': level,
                    'start_date': emp_data['start_date'],
                    'job_title': emp_data['job_title'],
                    'birth_date': emp_data['birth_date'],
                    'insurance_number': emp_data['insurance_number']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully added {emp.username}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'{emp.username} already exists'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully seeded Employee data'))
