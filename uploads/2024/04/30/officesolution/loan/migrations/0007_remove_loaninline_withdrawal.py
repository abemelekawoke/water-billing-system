# Generated by Django 5.0.4 on 2024-04-22 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0006_remove_loaninline_balance_loan_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loaninline',
            name='Withdrawal',
        ),
    ]
