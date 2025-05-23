# Generated by Django 5.1.3 on 2024-12-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setups', '0033_alter_academicformula_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorshipType',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Sponsorship types',
            },
        ),
        migrations.CreateModel(
            name='TransportCategory',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Transport categories',
            },
        ),
    ]
