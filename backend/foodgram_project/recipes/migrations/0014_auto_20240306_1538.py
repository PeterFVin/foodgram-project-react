# Generated by Django 3.2.16 on 2024-03-06 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0013_auto_20240228_1934"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.ingredient",
                verbose_name="ingredient",
            ),
        ),
        migrations.AlterField(
            model_name="ingredientrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_list",
                to="recipes.recipe",
                verbose_name="recipe",
            ),
        ),
        migrations.AlterField(
            model_name="tagrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.recipe",
                verbose_name="recipe",
            ),
        ),
        migrations.AlterField(
            model_name="tagrecipe",
            name="tag",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.tag",
                verbose_name="tag",
            ),
        ),
    ]
