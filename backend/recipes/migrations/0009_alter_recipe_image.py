# Generated by Django 3.2.16 on 2024-01-31 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0008_auto_20240126_2056"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                default="default.jpg",
                upload_to="recipe_images/",
                verbose_name="изображение",
            ),
        ),
    ]
