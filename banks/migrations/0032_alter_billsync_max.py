# Generated by Django 5.2.1 on 2025-05-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0031_billsync_max'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billsync',
            name='max',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
