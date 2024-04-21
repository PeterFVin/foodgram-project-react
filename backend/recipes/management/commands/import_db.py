import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загружаем список ингредиентов в БД"

    def handle(self, *args, **kwargs):
        """Загрузка ингредиентов в БД"""
        try:
            self.stdout.write("Начало загрузки ингредиентов!")
            file_path = os.path.join(
                settings.BASE_DIR,
                "data",
                "ingredients.csv")
            with open(
                file_path,
                encoding="utf-8",
            ) as file:
                reader = csv.reader(file)
                next(reader)
                for box1, box2 in reader:
                    Ingredient.objects.get_or_create(
                        name=box1,
                        measurement_unit=box2)
            self.stdout.write("Ингредиенты загружены успешно!")
        except FileNotFoundError:
            self.stdout.write("Файл отсутствует в директории data")
