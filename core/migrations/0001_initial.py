# Generated by Django 4.1.1 on 2022-10-29 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=15, verbose_name='Fisrt name')),
                ('last_name', models.CharField(max_length=15, verbose_name='Last name')),
                ('number', models.CharField(max_length=15, verbose_name='Contact number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.CharField(max_length=200, verbose_name='Message')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
