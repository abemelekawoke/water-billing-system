# Generated by Django 5.1.7 on 2025-03-26 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0017_alter_bankupload_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankupload',
            options={'managed': False},
        ),
    ]
