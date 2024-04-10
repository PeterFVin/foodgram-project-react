# Generated by Django 3.2.16 on 2024-04-09 16:59

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0023_auto_20240402_1930"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="favorite",
            options={
                "verbose_name": "избранный рецепт",
                "verbose_name_plural": "избранные рецепты",
            },
        ),
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "ordering": ("name",),
                "verbose_name": "ингредиент",
                "verbose_name_plural": "ингредиенты",
            },
        ),
        migrations.AlterModelOptions(
            name="ingredientrecipe",
            options={
                "ordering": ("recipe",),
                "verbose_name": "ингредиент в рецепте",
                "verbose_name_plural": "ингредиенты в рецепте",
            },
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("name", "author_id"),
                "verbose_name": "рецепт",
                "verbose_name_plural": "рецепты",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={
                "verbose_name": "список покупок",
                "verbose_name_plural": "списки покупок",
            },
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name": "тег", "verbose_name_plural": "теги"},
        ),
        migrations.AlterModelOptions(
            name="tagrecipe",
            options={
                "ordering": ("recipe",),
                "verbose_name": "тег в рецепте",
                "verbose_name_plural": "теги в рецепте",
            },
        ),
        migrations.AlterField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="measurement_unit",
            field=models.CharField(max_length=200, verbose_name="единица измерения"),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=200, verbose_name="название"),
        ),
        migrations.AlterField(
            model_name="ingredientrecipe",
            name="amount",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        9999, message="Максимальное значение 9999!"
                    ),
                    django.core.validators.MinValueValidator(
                        1, message="Минимальное значение 1!"
                    ),
                ],
                verbose_name="количество",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, message="Минимальное значение 1!"
                    ),
                    django.core.validators.MaxValueValidator(
                        720, message="Максимальное значение 720!"
                    ),
                ],
                verbose_name="время приготовления",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=200, verbose_name="рецепт"),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=colorfield.fields.ColorField(
                default="#FF0000",
                image_field=None,
                max_length=25,
                samples=None,
                unique=True,
                verbose_name="цвет",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=200, unique=True, verbose_name="тег"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(max_length=200, unique=True, verbose_name="slug"),
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("name", "measurement_unit"), name="unique_ingredient"
            ),
        ),
    ]
