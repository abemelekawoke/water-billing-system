# Generated by Django 5.1.4 on 2025-01-29 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0009_alter_inputdata_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialSaleReport',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('CODE', models.CharField(max_length=100)),
                ('KEBELE', models.CharField(max_length=100)),
                ('ZONE', models.CharField(max_length=100)),
                ('SERVICE', models.CharField(max_length=100)),
                ('CONSUMPTION', models.CharField(max_length=100)),
                ('TOTAL_PRICE', models.CharField(max_length=100)),
                ('MONTH', models.CharField(max_length=100)),
                ('YEAR', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'ቢል ዝግጅት ወራዊ ዝርዝር ሪፖርት',
                'verbose_name_plural': 'ቢል ዝግጅት ወራዊ ዝርዝር ሪፖርት',
                'db_table': 'HANDOVER_DETAILS_REPORT',
                'managed': False,
            },
        ),
    ]
