# Generated by Django 4.2 on 2024-11-14 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setups', '0023_alter_tuitionformula_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportFormula',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Fermata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.grade')),
            ],
            options={
                'verbose_name_plural': 'Transport formula',
            },
        ),
    ]
