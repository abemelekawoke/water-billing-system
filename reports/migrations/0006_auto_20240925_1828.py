# Generated by Django 3.2.25 on 2024-09-25 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20240925_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='revenueannualperformance',
            options={'managed': False, 'verbose_name': 'የገቢ አመታዊ ሪፖርት', 'verbose_name_plural': 'የገቢ አመታዊ ሪፖርት'},
        ),
        migrations.AlterModelOptions(
            name='revenuemonthlyperformance',
            options={'managed': False, 'verbose_name': 'የገቢ ወራዊ ሪፖርት', 'verbose_name_plural': 'የገቢ ወራዊ ሪፖርት'},
        ),
        migrations.AlterModelOptions(
            name='revenueperformancefromapriltojune',
            options={'managed': False, 'verbose_name': 'የገቢ 4ኛ ሩብ አመት ሪፖርት', 'verbose_name_plural': 'የገቢ 4ኛ ሩብ አመት ሪፖርት'},
        ),
        migrations.AlterModelOptions(
            name='revenueperformancefromjanuarytomarch',
            options={'managed': False, 'verbose_name': 'የገቢ 3ኛ ሩብ አመት ሪፖርት', 'verbose_name_plural': 'የገቢ 3ኛ ሩብ አመት ሪፖርት'},
        ),
        migrations.AlterModelOptions(
            name='revenueperformancefromjulytoseptember',
            options={'managed': False, 'verbose_name': 'የገቢ 1ኛ ሩብ አመት ሪፖርት', 'verbose_name_plural': 'የገቢ 1ኛ ሩብ አመት ሪፖርት'},
        ),
        migrations.AlterModelOptions(
            name='revenueperformancefromoctobertodecember',
            options={'managed': False, 'verbose_name': 'የገቢ 2ኛ ሩብ አመት ሪፖርት', 'verbose_name_plural': 'የገቢ 2ኛ ሩብ አመት ሪፖርት'},
        ),
        migrations.AlterModelTable(
            name='revenueperformancefromoctobertodecember',
            table='"Revenue_from_October_to_December"',
        ),
    ]
