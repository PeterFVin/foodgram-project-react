# Generated by Django 3.2.16 on 2024-03-23 17:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0017_auto_20240321_1719"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="Минимальное значение 1!"
                    )
                ],
                verbose_name="время приготовления",
            ),
        ),
    ]
