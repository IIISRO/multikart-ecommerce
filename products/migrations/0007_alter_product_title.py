# Generated by Django 4.1.1 on 2022-11-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_category_slug_az_remove_category_slug_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
