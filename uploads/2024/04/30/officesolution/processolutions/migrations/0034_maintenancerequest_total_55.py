# Generated by Django 3.1 on 2020-09-01 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processolutions', '0033_auto_20200901_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='Total_55',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
