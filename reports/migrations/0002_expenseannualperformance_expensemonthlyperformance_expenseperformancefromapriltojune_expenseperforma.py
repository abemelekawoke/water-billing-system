# Generated by Django 3.2.25 on 2024-09-23 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseAnnualPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Expense_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የወጪ አመታዊ ሪፖርት',
                'db_table': 'Expense_annual_performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseMonthlyPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Month', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Expense_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የወጪ ወራዊ ሪፖርት',
                'db_table': 'Expense_monthly_performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExpensePerformanceFromAprilToJune',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Expense_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የወጪ 4ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Expense_from_April_to_June',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExpensePerformanceFromJanuaryToMarch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Expense_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የወጪ 3ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Expense_from_January_to_March',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExpensePerformanceFromJulyToSeptember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Expense_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የወጪ 1ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Expense_from_July_to_September',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExpensePerformanceFromOctoberToDecember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Expense_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የወጪ 2ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Expense_from_October_to_December',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PotableWaterAnnualPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Year', models.CharField(max_length=150)),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Service_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የመጠጥ ውሃ አመታዊ ሪፖርት',
                'db_table': 'Potable_water_annual_performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PotableWaterMonthlyPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Month', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Service_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የመጠጥ ውሃ ወራዊ ሪፖርት',
                'db_table': 'Potable_water_monthly_performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PotableWaterPerformanceFromAprilToJune',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Year', models.CharField(max_length=150)),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Service_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የመጠጥ ውሃ 4ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Potable_water_from_April_to_June',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PotableWaterPerformanceFromJanuaryToMarch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Year', models.CharField(max_length=150)),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Service_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የመጠጥ ውሃ 3ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Potable_water_from_January_to_March',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PotableWaterPerformanceFromJulyToSeptember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Year', models.CharField(max_length=150)),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Service_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የመጠጥ ውሃ 1ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Potable_water_from_July_to_September',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PotableWaterPerformanceFromOctoberToDecember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Year', models.CharField(max_length=150)),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Service_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የመጠጥ ውሃ 2ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Potable_water_from_October_to_December',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RevenueAnnualPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Revenue_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የገቢ አመታዊ ሪፖርት',
                'db_table': 'Revenue_annual_performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RevenueMonthlyPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Month', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Revenue_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የገቢ ወራዊ ሪፖርት',
                'db_table': 'Revenue_monthly_performance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RevenuePerformanceFromAprilToJune',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Revenue_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የገቢ 4ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Revenue_from_April_to_June',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RevenuePerformanceFromJanuaryToMarch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Revenue_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የገቢ 3ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Revenue_from_January_to_March',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RevenuePerformanceFromJulyToSeptember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Revenue_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የገቢ 1ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Revenue_from_July_to_September',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RevenuePerformanceFromOctoberToDecember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Code', models.CharField(max_length=150)),
                ('Year', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Measurement', models.CharField(max_length=150)),
                ('Revenue_annual_plan', models.CharField(max_length=150)),
                ('Plan', models.CharField(max_length=150)),
                ('Performed', models.CharField(max_length=150)),
                ('Performance', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'የገቢ 2ኛ ሩብ አመት ሪፖርት',
                'db_table': 'Revenue_from_October_to_December',
                'managed': False,
            },
        ),
    ]
