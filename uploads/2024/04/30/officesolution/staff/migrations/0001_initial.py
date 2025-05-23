# Generated by Django 5.0.4 on 2024-04-13 08:46

import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('First_name', models.CharField(max_length=150)),
                ('Father_name', models.CharField(max_length=150)),
                ('Last_name', models.CharField(max_length=150)),
                ('Educational_level', models.CharField(max_length=150)),
                ('Position', models.CharField(max_length=150)),
                ('Employee_status', models.CharField(max_length=150)),
                ('Contact_number', models.CharField(max_length=150)),
                ('Registered_at', models.DateTimeField(auto_now=True, verbose_name='Registered at')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by4', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by4', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
