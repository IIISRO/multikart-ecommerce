# Generated by Django 4.1.1 on 2022-12-14 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_main_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_img',
            field=models.ImageField(upload_to='product_img'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='productimg',
            name='image',
            field=models.ImageField(upload_to='product_img'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_banner',
            field=models.ImageField(upload_to='vendor_img'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_img',
            field=models.ImageField(upload_to='vendor_img'),
        ),
    ]
