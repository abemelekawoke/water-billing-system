# Generated by Django 3.1 on 2020-08-28 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processolutions', '0006_auto_20200828_0608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financecostplan',
            name='Month',
        ),
        migrations.RemoveField(
            model_name='financecostplan',
            name='Year',
        ),
        migrations.RemoveField(
            model_name='financeincomeplan',
            name='Month',
        ),
        migrations.RemoveField(
            model_name='financeincomeplan',
            name='Year',
        ),
        migrations.RemoveField(
            model_name='humanresourceplan',
            name='Month',
        ),
        migrations.RemoveField(
            model_name='humanresourceplan',
            name='Year',
        ),
        migrations.RemoveField(
            model_name='planningandcustomerissueplan',
            name='Month',
        ),
        migrations.RemoveField(
            model_name='planningandcustomerissueplan',
            name='Year',
        ),
        migrations.RemoveField(
            model_name='watersupplyplan',
            name='Month',
        ),
        migrations.RemoveField(
            model_name='watersupplyplan',
            name='Year',
        ),
        migrations.AddField(
            model_name='financecostperformed',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='financecostplan',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='financeincomeperformed',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='financeincomeplan',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generalleisure',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='humanresourceperformed',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='humanresourceplan',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planningandcustomerissueperformed',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planningandcustomerissueplan',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='watersupplyplan',
            name='Dates',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
