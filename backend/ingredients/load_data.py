import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load data from CSV file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        from .models import Ingredient
        csv_file = options['csv_file']
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            ingredients = []
            for row in reader:
                name, unit = row
                ingredients.append(
                    Ingredient(name=name, measurement_unit=unit)
                )
            Ingredient.objects.bulk_create(ingredients)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
