import csv
import os

from reviews.models import Ingredient


script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, '../data/ingredients.csv')
with open(file, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        Ingredient.objects.get_or_create(
            name=row[0], measurement_unit=row[1]
        )
print('uploaded successfully')