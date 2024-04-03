import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import Tag

DATA_ROOT = os.path.join(settings.BASE_DIR, "data")


class Command(BaseCommand):
    help = "load tags.json into db"

    # def add_arguments(self, parser):
    #     parser.add_argument('filename', default='tags.json', nargs='?',
    #                         type=str)

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "data", "tags.json")
        try:
            with open(
                file_path,
                encoding="utf-8",
            ) as file:
                data = json.load(file)
                for tag in data:
                    try:
                        Tag.objects.create(
                            name=tag["name"],
                            color=tag["color"],
                            slug=tag["slug"],
                        )
                    except IntegrityError:
                        self.stdout.write("Нелья добавить.")
        except FileNotFoundError:
            self.stdout.write("Файл отсутствует в директории data")
