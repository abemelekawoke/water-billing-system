# Generated by Django 3.1 on 2020-08-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processolutions', '0007_auto_20200828_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='watersupplyperformed',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
