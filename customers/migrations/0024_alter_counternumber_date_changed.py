# Generated by Django 5.1.7 on 2025-03-29 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0023_remove_client_counter_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counternumber',
            name='date_changed',
            field=models.DateField(),
        ),
    ]
