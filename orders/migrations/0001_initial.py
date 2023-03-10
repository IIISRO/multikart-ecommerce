# Generated by Django 4.1.1 on 2022-10-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.IntegerField()),
                ('product', models.IntegerField()),
                ('property', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
