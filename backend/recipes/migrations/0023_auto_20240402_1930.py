# Generated by Django 3.2.16 on 2024-04-02 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0022_alter_ingredientrecipe_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="measurement_unit",
            field=models.CharField(max_length=300, verbose_name="единица измерения"),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=300, verbose_name="название"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=300, unique=True, verbose_name="тег"),
        ),
    ]
