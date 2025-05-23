# Generated by Django 5.0.4 on 2024-04-18 14:39

import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Date', models.DateTimeField()),
                ('Registered_at', models.DateTimeField(auto_now=True, verbose_name='Registered at')),
                ('Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staffprofile')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by19', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by19', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanInline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Date', models.DateTimeField()),
                ('Deposite', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('Withdrawal', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('Balance', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('Registered_at', models.DateTimeField(auto_now=True, verbose_name='Registered at')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='re_by', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upd_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='BankBook',
        ),
    ]
