# Generated by Django 3.2.16 on 2024-03-27 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_remove_ingredientrecipe_unique_recipe_ingredient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name_plural': 'рецепты'},
        ),
    ]