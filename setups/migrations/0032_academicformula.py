# Generated by Django 5.1.3 on 2024-11-20 04:34

import django.db.models.deletion
import setups.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setups', '0031_alter_penaltyschool_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicFormula',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('academic_year', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='የትምህርት ዘመን')),
                ('pass_mark', models.DecimalField(decimal_places=2, max_digits=15)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.grade')),
            ],
            options={
                'verbose_name_plural': 'Tuition formula',
            },
        ),
    ]
