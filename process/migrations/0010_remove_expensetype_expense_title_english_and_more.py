# Generated by Django 5.1.7 on 2025-03-23 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0009_remove_potablewaterservicetype_service_title_english_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expensetype',
            name='Expense_title_english',
        ),
        migrations.RemoveField(
            model_name='revenuetype',
            name='Revenue_title_english',
        ),
    ]
