# Generated by Django 4.1.1 on 2023-01-15 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
