import csv

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from CSV file into database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                name, unit = row
                product = Ingredient(name=name, measurement_unit=unit)
                product.save()
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
