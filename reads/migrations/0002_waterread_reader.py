# Generated by Django 3.2.25 on 2024-07-27 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setups', '0006_auto_20240727_1143'),
        ('reads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterread',
            name='reader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='setups.reader'),
        ),
    ]
