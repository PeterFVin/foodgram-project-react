# Generated by Django 3.2.16 on 2023-12-28 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20231227_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ingredient_list', to='recipes.recipe', verbose_name='recipe_id'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipe', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='recipes.TagRecipe', to='recipes.Tag'),
        ),
    ]
