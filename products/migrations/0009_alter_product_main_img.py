# Generated by Django 4.1.1 on 2022-12-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_main_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_img',
            field=models.ImageField(upload_to='static/assets/media/product_img'),
        ),
    ]
