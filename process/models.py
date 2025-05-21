from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
from django.db import models
from django.utils import timezone
from decimal import Decimal
import datetime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from setups.models import *
from stocks.models import *
from employees.models import *

from smart_selects.db_fields import ChainedForeignKey

class GeneralLeisure(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Tasks = models.CharField(max_length = 150)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Month = models.ForeignKey(Month, on_delete=models.CASCADE)
    General = models.PositiveIntegerField(default=0)
    Check_no = models.PositiveIntegerField(default=0)
    Check_payable = models.PositiveIntegerField(default=0)
    Receipt_no = models.CharField(max_length = 250,default=0)
    Deposit = models.DecimalField(decimal_places=2, max_digits=25, default=0)
    Withdraw = models.DecimalField(decimal_places=2, max_digits=25, default=0)
    Balance = models.DecimalField(decimal_places=2, max_digits=25, default=0)
    Registered_date = models.CharField(max_length=150, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by1111")
    Registered_by = CurrentUserField(related_name="pl_by1111")
    def __str__(self):
        return "%s" % (self.Tasks)
    class Meta:
        verbose_name="General leisure"
        verbose_name_plural="General leisure"

    def save(self, *args, **kwargs):
        try:
            previous_balance = GeneralLeisure.objects.latest('id').Balance
        except ObjectDoesNotExist:
            # If no BankBook records exist, set previous_balance to 0
            previous_balance = 0

        # Ensure previous_balance is not None
        if previous_balance is None:    
            previous_balance = 0

        # Update balance based on previous balance, deposite, and withdrawal
        self.Balance = previous_balance + self.Deposit - self.Withdraw

        super(GeneralLeisure, self).save(*args, **kwargs)
        
class RevenueType(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Code = models.CharField(max_length = 150)
    Revenue_title_amharic = ChainedForeignKey(
        Task,
        chained_field="department", 
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    # Revenue_title_amharic = models.ForeignKey(Task, on_delete=models.CASCADE)
    # Revenue_title_english = models.CharField(max_length = 150, default='None')

    Revenue_annual_plan = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)

    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by11111")
    Registered_by = CurrentUserField(related_name="pl_by11111")
  
    def __str__(self):
        return "%s" % (self.Code)

    class Meta:
        verbose_name="Revenue plan"
        verbose_name_plural="Revenue plan"

class AllRevenue(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.ForeignKey(RevenueType, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2, max_digits=25, default=0)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Month = models.ForeignKey(Month, on_delete=models.CASCADE)

    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by111111")
    Registered_by = CurrentUserField(related_name="pl_by111111")

    def __str__(self):
        return "%s" % (self.Code)

    class Meta:
        verbose_name="Revenue performed"
        verbose_name_plural="Revenue performed"

    # def save(self, *args, **kwargs):
    #     br = RevenueReport.objects.get(id=self.Code_id)
    #     getbal = br.Balances
    #     if getbal == None:
    #         getbal=0
    #     self.Balance = getbal + self.Amount
    #     super(AllRevenue, self).save(*args, **kwargs)

class ExpenseType(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Code = models.CharField(max_length = 150)
    Expense_title_amharic = ChainedForeignKey(
        Task,
        chained_field="department", 
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    # Expense_title_english = models.CharField(max_length = 150, default='None')

    Expense_annual_plan = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)

    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by1111111")
    Registered_by = CurrentUserField(related_name="pl_by1111111")

    def __str__(self):
        return "%s" % (self.Code)

    class Meta:
        verbose_name="Expense plan"
        verbose_name_plural="Expense plan"

class AllExpense(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2, max_digits=25, default=0)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Month = models.ForeignKey(Month, on_delete=models.CASCADE)

    Registered_date = models.CharField(max_length=150, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by11111111")
    Registered_by = CurrentUserField(related_name="pl_by11111111")

    def __str__(self):
        return "%s" % (self.Code)

    class Meta:
        verbose_name="Expense performed"
        verbose_name_plural="Expense performed" 

    # def save(self, *args, **kwargs):
    #     br = ExpenseReport.objects.get(id=self.Code_id)
    #     getbal = br.Balances
    #     if getbal == None:
    #         getbal=0
    #     self.Balance = getbal + self.Amount
    #     super(AllExpense, self).save(*args, **kwargs)

class PotableWaterServiceType(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Service_title_amharic  = ChainedForeignKey(
        Task,
        chained_field="department", 
        chained_model_field="department",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    # Service_title_english = models.CharField(max_length = 150, default='None')

    Service_annual_plan = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)

    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="upb1")
    Registered_by = CurrentUserField(related_name="rb1")

    def __str__(self):
        return "%s" % (self.Service_title_amharic)

    class Meta:
        verbose_name="Potable water service plan"
        verbose_name_plural="Potable water service plan"

class AllPotableWaterServiceManagement(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Dates = models.DateField('Date')
    Code = models.ForeignKey(PotableWaterServiceType, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2, max_digits=25, default=0)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Month = models.ForeignKey(Month, on_delete=models.CASCADE)

    Registered_date = models.CharField(max_length=150,verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by1111113")
    Registered_by = CurrentUserField(related_name="pl_by1111116")

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Potable water service performed"
        verbose_name_plural="potable water service performed"


class DetailCostManagement(models.Model):
    THEME_CHOICES1 = (
        ('Residence', 'Residence'),
        ('Trade_organization', 'Trade organization'),
        ('Public_government', 'Public government'),
    )

    THEME_CHOICES2 = (
        ('Pendind', 'Pendind'),
        ('On process', 'On process'),
        ('Completed', 'Completed'),
    )

    id = models.AutoField(primary_key=True, unique=True)
    Full_name = models.CharField(max_length=150)
    Kebele = models.CharField(max_length=150)
    House_number = models.CharField(max_length=150, blank=True)
    Customer_type = models.CharField(max_length=150, choices=THEME_CHOICES1, default='None')
    Customer_neighbor = models.CharField(max_length=150, blank=True)

    Address = models.CharField(max_length=150)
    Phone_number = models.CharField(max_length=150)
    Place = models.CharField(max_length=150)
    Line_joined = models.CharField(max_length=150)

    Year = models.ForeignKey(Year, on_delete=models.CASCADE)
    Month = models.ForeignKey(Month, on_delete=models.CASCADE)

    Officer = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    Process_status = models.CharField(max_length=150, choices=THEME_CHOICES2, null=True, blank=True, default='Pendind')

    For_consultation = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    For_information = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    Deposite = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    For_Digging = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    For_Rope = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    For_Agreement = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    For_Forms = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    Total_Form = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)

    Material_cost = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    Total_60 = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    Total_25 = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)

    Grand_total = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)

    Potable_water = models.CharField(max_length=250, blank=True, default="To Income Officer")
    Income_office = models.CharField(max_length=250, blank=True, default="To Finance Officer")
    Amount = models.DecimalField(max_digits=25, decimal_places=2, blank=True, default=0)
    Cashier = models.CharField(max_length=250, blank=True, default="በገቢ ደረሰኝ ቁጥር       ብር ስለከፈለ ቀሪው ስራ ታይቶ ይሰራለት፡፡")

    Requested_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up61")
    Registered_by = CurrentUserField(related_name="pby61")

    def __str__(self):
        return "%s" % (self.id)

    class Meta():
        verbose_name_plural = "Detail cost"

    def save(self, *args, **kwargs):
        invoice_lines = MaterialInline.objects.filter(Detail_cost_management=self.id)
        self.Material_cost = 0
        for line in invoice_lines:
            self.Material_cost += line.Total_price
            self.Total_25 = (self.Material_cost * 25)/100
            self.Total_60 = (self.Material_cost * 60)/100
            self.Grand_total = self.Material_cost + self.Total_25 + self.Total_60 + self.Deposite + self.For_Digging + self.For_Rope + self.For_Agreement + self.For_Forms + self.For_consultation + self.For_information

        super(DetailCostManagement, self).save(*args, **kwargs)

# class ServiceTypeInline(models.Model):
#     id = models.AutoField(primary_key=True, unique=True)
#     All_potable_water_service = models.ForeignKey(AllPotableWaterServiceManagement, on_delete=models.CASCADE)
#     Service_type = models.ForeignKey(PotableWaterServiceType, on_delete=models.CASCADE)
#     Quantity = models.DecimalField(max_digits = 11, decimal_places = 2, default=1)

#     def __str__(self):
#         return "%s" % (self.id)

#     class Meta:
#         verbose_name = "Service type"
#         verbose_name_plural = "Service types"

    
class MaterialInline(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    Detail_cost_management = models.ForeignKey(DetailCostManagement, on_delete=models.CASCADE)
    Name = models.ForeignKey(StockManagement, on_delete=models.CASCADE)
    # Inch = models.CharField(max_length = 150, choices = THEME_CHOICES,blank=True)
    Quantity = models.DecimalField(max_digits = 11, decimal_places = 2)
    Single_price = models.DecimalField(max_digits = 11, decimal_places = 2)
    Total_price = models.DecimalField(max_digits = 11, decimal_places = 2, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            p = StockManagement.objects.get(id=self.Name_id)  # Ensure correct lookup
            self.Single_price = p.Individual_price
            self.Total_price = self.Quantity * self.Single_price
        except StockManagement.DoesNotExist:
            self.Single_price = 0
            self.Total_price = 0

        super(MaterialInline, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Detail Material"
        verbose_name_plural = "Detail Materials"

    # def save(self, *args, **kwargs):
    #     p = StockManagement.objects.get(Name=self.Name_id)
    #     ssp = p.Individual_price
    #     self.Single_price = ssp

    #     self.Total_price = self.Quantity * ssp
    #     super(MaterialInline, self).save(*args, **kwargs)

    # class Meta:
    #     verbose_name = "Detail Material"
    #     verbose_name_plural = "Detail Materials"

# class DetailCostRequestPotableWater(DetailCostRequest):

#     class Meta:
#         proxy = True
#         verbose_name_plural='ለመጠጥ ዉኃ የስራ ሂደት 60% አገልግሎት ክፍያ ጥያቄ'

# class DetailCostRequestIncomeOfficer(DetailCostRequest):

#     class Meta:
#         proxy = True
#         verbose_name_plural='ለገቢ ግዥ ፋይናንስ የስራ ሂደት 60% አገልግሎት ክፍያ ጥያቄ'

# class DetailCostRequestCashier(DetailCostRequest):

#     class Meta:
#         proxy = True
#         verbose_name_plural='ለንብረትና ገንዘብ ያዥ የስራ ሂደት 60% አገልግሎት ክፍያ ጥያቄ'

class DepartmentPerformanceRank(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    department = models.CharField(max_length = 150)
    month = models.CharField(max_length = 150)
    year = models.CharField(max_length = 150)
    total_plan = models.CharField(max_length = 150) 
    total_performed = models.CharField(max_length = 150) 
    performance_percentage = models.CharField(max_length = 150)
    rank = models.CharField(max_length=100)
 
    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የስራ ሂደት የአፈጻጸም ደረጃ"
        verbose_name_plural = "የስራ ሂደት የአፈጻጸም ደረጃ"
        db_table = "DEPARTMENTPERFORMANCERANK"