# Generated by Django 4.1.1 on 2022-11-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_profile_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='card',
            field=models.CharField(blank=True, default='', max_length=16, null=True),
        ),
    ]