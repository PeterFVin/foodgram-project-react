import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружаем список ингредиентов в БД'

    def handle(self, *args, **kwargs):
        print('Начинаем загрузку ингредиентов в БД!')
        """Загрузка ингредиентов в БД"""
        with open('C:/Dev/foodgram-project-react/data/ingredients.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                ingredient = Ingredient(
                    name=row[0],
                    measurement_unit=row[1]
                )
                ingredient.save()
        print('Delicious. Finally, some good f**king food')
