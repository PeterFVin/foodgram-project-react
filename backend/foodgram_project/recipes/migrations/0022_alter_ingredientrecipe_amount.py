# Generated by Django 3.2.16 on 2024-03-28 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0021_alter_recipe_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientrecipe",
            name="amount",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="должен быть хотя бы один ингредиент!"
                    )
                ],
                verbose_name="количество",
            ),
        ),
    ]
