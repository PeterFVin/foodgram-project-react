import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загружаем список ингредиентов в БД"

    def handle(self, *args, **kwargs):
        print("Начинаем загрузку ингредиентов в БД!")
        """Загрузка ингредиентов в БД"""

        file_path = os.path.join(settings.BASE_DIR, "data", "ingredients.csv")
        with open(
            file_path,
            encoding="utf-8",
        ) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                ingredient = Ingredient(name=row[0], measurement_unit=row[1])
                ingredient.save()
        print("Delicious. Finally, some good f**king food")
