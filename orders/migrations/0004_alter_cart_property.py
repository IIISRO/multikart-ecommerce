# Generated by Django 4.1.1 on 2023-01-15 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_rename_sale_price_product_actual_price'),
        ('orders', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='property',
            field=models.ManyToManyField(related_name='carts', to='products.propertyvalue'),
        ),
    ]
