# Generated by Django 3.2.16 on 2024-04-19 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0026_alter_recipe_author"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="tags",
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipes", to="recipes.Tag", verbose_name="теги"
            ),
        ),
        migrations.DeleteModel(
            name="TagRecipe",
        ),
    ]
