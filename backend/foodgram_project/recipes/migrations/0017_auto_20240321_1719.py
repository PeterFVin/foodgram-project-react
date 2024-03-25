# Generated by Django 3.2.16 on 2024-03-21 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20240321_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name_plural': 'избранное'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name_plural': 'ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('name',), 'verbose_name_plural': 'рецепты'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name_plural': 'список покупок'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': 'теги'},
        ),
    ]
