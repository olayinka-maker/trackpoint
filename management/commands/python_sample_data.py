from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trackpoint.models import Department, Staff, AssetType, Asset
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Create departments
        dept_names = ['IT', 'Finance', 'HR', 'Operations']
        departments = []
        for name in dept_names:
            dept, created = Department.objects.get_or_create(name=name)
            departments.append(dept)

        # Create asset types
        asset_types_data = [
            ('Gadget', '#ff6b8a'),
            ('Furniture', '#4ecdc4'),
            ('Electronic', '#ffe66d'),
        ]
        asset_types = []
        for name, color in asset_types_data:
            at, created = AssetType.objects.get_or_create(
                name=name, defaults={'color': color})
            asset_types.append(at)

        # Create users and staff
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'staff{i+1}',
                defaults={
                    'first_name': f'Employee',
                    'last_name': f'{i+1}',
                    'email': f'staff{i+1}@company.com'
                })
            if created:
                Staff.objects.create(user=user,
                                     department=random.choice(departments),
                                     position=random.choice([
                                         'Manager', 'Analyst', 'Coordinator',
                                         'Specialist'
                                     ]),
                                     hire_date=date.today() -
                                     timedelta(days=random.randint(30, 1000)))

        # Create assets
        staff_members = list(Staff.objects.all())
        asset_names = [
            'Laptop Dell XPS', 'iPhone 15', 'Standing Desk', 'Office Chair',
            'Monitor 27"', 'Wireless Mouse', 'Keyboard', 'Tablet iPad'
        ]

        for i, name in enumerate(asset_names):
            Asset.objects.get_or_create(
                name=name,
                defaults={
                    'asset_type':
                    random.choice(asset_types),
                    'department':
                    random.choice(departments),
                    'assigned_to':
                    random.choice(staff_members)
                    if random.choice([True, False]) else None,
                    'serial_number':
                    f'SN{1000+i}',
                    'purchase_date':
                    date.today() - timedelta(days=random.randint(1, 365)),
                    'purchase_price':
                    random.uniform(100, 2000),
                    'status':
                    random.choice(['active', 'maintenance', 'retired'])
                })

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully populated database with sample data'))
