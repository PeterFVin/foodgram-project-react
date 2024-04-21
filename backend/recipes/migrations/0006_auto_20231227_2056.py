# Generated by Django 3.2.16 on 2023-12-27 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_auto_20231223_1648"),
    ]

    operations = [
        migrations.AddField(
            model_name="ingredientrecipe",
            name="amount",
            field=models.IntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="должен быть хотя бы один ингредиент!"
                    )
                ],
                verbose_name="количество",
            ),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="ingredientrecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe_id", "ingredient_id"),
                name="unique_recipe_ingredient",
            ),
        ),
    ]