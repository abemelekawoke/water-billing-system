# Generated by Django 5.1.7 on 2025-03-31 02:40

import django.db.models.deletion
import employees.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_staffprofile_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(default=employees.models.EmployeePerformance.get_current_month, max_length=50)),
                ('year', models.CharField(default=employees.models.EmployeePerformance.get_current_year, max_length=50)),
                ('score', models.FloatField()),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_scores', to='employees.staffprofile')),
            ],
            options={
                'ordering': ['-year'],
                'unique_together': {('staff', 'year')},
            },
        ),
    ]
