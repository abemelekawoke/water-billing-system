# Generated by Django 5.0.6 on 2024-06-14 21:54

import customers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_client_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='month',
            field=models.CharField(default=customers.models.Client.get_current_month, max_length=50),
        ),
        migrations.AddField(
            model_name='client',
            name='year',
            field=models.CharField(default=customers.models.Client.get_current_year, max_length=50),
        ),
    ]
