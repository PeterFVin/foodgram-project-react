# Generated by Django 3.2.16 on 2023-12-23 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20231223_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='recipe_images/',
                verbose_name='изображение',
            ),
        ),
    ]
