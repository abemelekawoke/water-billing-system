# Generated by Django 5.1.7 on 2025-04-01 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0025_remove_client_amharic_father_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='code',
            field=models.CharField(default='DRB-', max_length=100, unique=True),
        ),
    ]
