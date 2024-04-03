# Generated by Django 3.2.16 on 2024-01-26 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0007_auto_20231228_1447"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredientrecipe",
            options={"ordering": ("recipe",)},
        ),
        migrations.AlterModelOptions(
            name="tagrecipe",
            options={"ordering": ("recipe",)},
        ),
        migrations.RemoveConstraint(
            model_name="ingredientrecipe",
            name="unique_recipe_ingredient",
        ),
        migrations.RemoveField(
            model_name="ingredientrecipe",
            name="ingredient_id",
        ),
        migrations.RemoveField(
            model_name="ingredientrecipe",
            name="recipe_id",
        ),
        migrations.RemoveField(
            model_name="tagrecipe",
            name="recipe_id",
        ),
        migrations.RemoveField(
            model_name="tagrecipe",
            name="tag_id",
        ),
        migrations.AddField(
            model_name="ingredientrecipe",
            name="ingredient",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="recipes.ingredient",
                verbose_name="ingredient",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ingredientrecipe",
            name="recipe",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="ingredient_list",
                to="recipes.recipe",
                verbose_name="recipe",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tagrecipe",
            name="recipe",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="recipes.recipe",
                verbose_name="recipe",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tagrecipe",
            name="tag",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="recipes.tag",
                verbose_name="tag",
            ),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="ingredientrecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="unique_recipe_ingredient",
            ),
        ),
    ]
