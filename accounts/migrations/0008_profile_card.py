# Generated by Django 4.1.1 on 2022-11-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_address_alter_profile_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='card',
            field=models.CharField(max_length=16, null=True),
        ),
    ]