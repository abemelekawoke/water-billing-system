# Generated by Django 5.1.7 on 2025-03-20 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0009_billsync_bank_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billsyncfile',
            old_name='upload_date',
            new_name='download_date',
        ),
        migrations.RenameField(
            model_name='billsyncfile',
            old_name='uploaded_file',
            new_name='downloaded_file',
        ),
    ]
