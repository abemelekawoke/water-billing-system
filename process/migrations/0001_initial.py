# Generated by Django 3.2.25 on 2024-09-14 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0001_initial'),
        ('stocks', '0001_initial'),
        ('setups', '0009_itemlists_measurement'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailCostManagement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Full_name', models.CharField(max_length=150)),
                ('Kebele', models.CharField(max_length=150)),
                ('House_number', models.CharField(blank=True, max_length=150)),
                ('Customer_type', models.CharField(choices=[('Residence', 'Residence'), ('Trade_organization', 'Trade organization'), ('Public_government', 'Public government')], default='None', max_length=150)),
                ('Customer_neighbor', models.CharField(blank=True, max_length=150)),
                ('Address', models.CharField(max_length=150)),
                ('Phone_number', models.CharField(max_length=150)),
                ('Place', models.CharField(max_length=150)),
                ('Line_joined', models.CharField(max_length=150)),
                ('Process_status', models.CharField(blank=True, choices=[('Pendind', 'Pendind'), ('On process', 'On process'), ('Completed', 'Completed')], default='Pendind', max_length=150, null=True)),
                ('For_consultation', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('For_information', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Deposite', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('For_Digging', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('For_Rope', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('For_Agreement', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('For_Forms', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Total_Form', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Material_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True)),
                ('Total_60', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Total_25', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Grand_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Potable_water', models.CharField(blank=True, default='To Income Officer', max_length=250)),
                ('Income_office', models.CharField(blank=True, default='To Finance Officer', max_length=250)),
                ('Amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25)),
                ('Cashier', models.CharField(blank=True, default='በገቢ ደረሰኝ ቁጥር       ብር ስለከፈለ ቀሪው ስራ ታይቶ ይሰራለት፡፡', max_length=250)),
                ('Requested_at', models.DateTimeField(auto_now=True, verbose_name='Registered at')),
                ('Month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.month')),
                ('Officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.staffprofile')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pby61', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up61', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name_plural': 'Detail cost management',
            },
        ),
        migrations.CreateModel(
            name='RevenueType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Code', models.CharField(max_length=150)),
                ('Revenue_title_amharic', models.CharField(max_length=150)),
                ('Revenue_title_english', models.CharField(default='None', max_length=150)),
                ('Revenue_annual_plan', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.measurement')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by11111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by11111', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'Revenue type management',
                'verbose_name_plural': 'Revenue type management',
            },
        ),
        migrations.CreateModel(
            name='PotableWaterServiceType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Service_title_amharic', models.CharField(max_length=150)),
                ('Service_title_english', models.CharField(default='None', max_length=150)),
                ('Service_annual_plan', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.measurement')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rb1', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upb1', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'Potable water service type management',
                'verbose_name_plural': 'Potable water service type management',
            },
        ),
        migrations.CreateModel(
            name='MaterialInline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Quantity', models.DecimalField(decimal_places=2, max_digits=11)),
                ('Single_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('Total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('Detail_cost_management', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.detailcostmanagement')),
                ('Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stockmanagement')),
            ],
            options={
                'verbose_name': 'Detail Material',
                'verbose_name_plural': 'Detail Materials',
            },
        ),
        migrations.CreateModel(
            name='GeneralLeisure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Tasks', models.CharField(max_length=150)),
                ('General', models.PositiveIntegerField(default=0)),
                ('Check_no', models.PositiveIntegerField(default=0)),
                ('Check_payable', models.PositiveIntegerField(default=0)),
                ('Receipt_no', models.CharField(default=0, max_length=250)),
                ('Deposit', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Withdraw', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Balance', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.month')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by1111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by1111', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'General leisure management',
                'verbose_name_plural': 'General leisure management',
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Code', models.CharField(max_length=150)),
                ('Expense_title_amharic', models.CharField(max_length=150)),
                ('Expense_title_english', models.CharField(default='None', max_length=150)),
                ('Expense_annual_plan', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.measurement')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by1111111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by1111111', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'Expense type management',
                'verbose_name_plural': 'Expense type management',
            },
        ),
        migrations.CreateModel(
            name='AllRevenue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Amount', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.revenuetype')),
                ('Month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.month')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by111111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by111111', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'All Revenue management',
                'verbose_name_plural': 'All Revenue management',
            },
        ),
        migrations.CreateModel(
            name='AllPotableWaterServiceManagement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Amount', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.potablewaterservicetype')),
                ('Month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.month')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by1111116', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by1111113', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'All potable water service management',
                'verbose_name_plural': 'All potable water service management',
            },
        ),
        migrations.CreateModel(
            name='AllExpense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Dates', models.DateField(verbose_name='Date')),
                ('Amount', models.DecimalField(decimal_places=2, default=0, max_digits=25)),
                ('Registered_date', models.CharField(max_length=150, verbose_name='Registered at')),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.expensetype')),
                ('Month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.month')),
                ('Registered_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pl_by11111111', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='up_by11111111', to=settings.AUTH_USER_MODEL)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setups.year')),
            ],
            options={
                'verbose_name': 'All Expense management',
                'verbose_name_plural': 'All Expense management',
            },
        ),
    ]
