# Generated by Django 4.1.1 on 2023-01-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_cart_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.FloatField(),
        ),
    ]
