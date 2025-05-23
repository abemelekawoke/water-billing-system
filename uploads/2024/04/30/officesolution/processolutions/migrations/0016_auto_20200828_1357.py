# Generated by Django 3.1 on 2020-08-28 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processolutions', '0015_auto_20200828_1352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expensetype',
            options={'verbose_name': 'Expense type management', 'verbose_name_plural': 'Expense type management'},
        ),
        migrations.AlterModelOptions(
            name='revenuetype',
            options={'verbose_name': 'Revenue type management', 'verbose_name_plural': 'Revenue type management'},
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='Registered_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by1111111', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='Updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by1111111', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Amount', models.DecimalField(decimal_places=2, default=0, max_digits=250)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processolutions.revenuetype')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by111111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by111111', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Revenue management',
                'verbose_name_plural': 'Revenue management',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Amount', models.DecimalField(decimal_places=2, default=0, max_digits=250)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processolutions.expensetype')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by11111111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by11111111', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Expense management',
                'verbose_name_plural': 'Expense management',
            },
        ),
    ]
