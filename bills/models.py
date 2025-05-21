from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from setups.models import *
from django.utils.html import format_html

# Create your models here.
   
class WaterBill(models.Model):
    status = (
        ('For_sale_by_bank', 'For Sale by Bank'),
        ('Sold_by_office', 'Sold by Office'),
    )
    id = models.AutoField(primary_key = True, unique = True)
    code = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100) 
    previous_read = models.PositiveBigIntegerField(help_text="ያለፈው ወር ንባብ",)	
    current_read = models.PositiveBigIntegerField(help_text="የዚህ ወር ንባብ")
    consumption = models.PositiveBigIntegerField(help_text="የዚህ ወር ፍጆታ")
    guage_rent = models.PositiveBigIntegerField(null=True, blank=True, help_text="የውኃ ቆጣሪ ኪራይ")
    
    block1 = models.PositiveBigIntegerField()
    block2 = models.PositiveBigIntegerField()
    block3 = models.PositiveBigIntegerField()
    block4 = models.PositiveBigIntegerField()
    block5 = models.PositiveBigIntegerField()
    current_price = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=25, decimal_places=2)
    bill_id = models.CharField(max_length=500)
    payment_start = models.DateField(null=True, blank=True)  # New field
    payment_end = models.DateField(null=True, blank=True)    # New field

    status = models.CharField(max_length=50, choices=status, default='For Sale by Bank')
    created_by = CurrentUserField(related_name="b1")
    created_at = models.DateField(auto_now=True)
    modified_by = CurrentUserField(related_name="mb1")
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Water bills {self.code} - {self.month}/{self.year}"   

def get_current_month():
    try:
        return Month.objects.get(status__iexact='Active')
    except Month.DoesNotExist:
        return Month.objects.none()  # Adjust as needed; ensure to handle cases when no Month is available

def get_current_year():
    try:
        return Year.objects.get(status__iexact='Active')
    except Year.DoesNotExist:
        return Year.objects.none()  # Adjust as needed; ensure to handle cases when no Year is available

class InputData(models.Model):
    kebele = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    month = models.CharField(max_length=50, default=get_current_month)
    year = models.CharField(max_length=50, default=get_current_year)

    def __str__(self):
        return f"Kebele: {self.kebele}, Zone: {self.zone}, Month: {self.month}, Year: {self.year}"
    
    class Meta:
        verbose_name = "Calculate bill"
        verbose_name_plural = "Calculate bills"
    
class UnsoldBills(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    code = models.CharField(max_length = 150)
    unsold_months = models.CharField(max_length = 150)
    unsold_price = models.CharField(max_length = 150)
    penalty = models.CharField(max_length = 150) 
    total_penalty = models.CharField(max_length = 150) 
    total_price = models.CharField(max_length = 150)
    # deposit = models.CharField(max_length=100)
    # clearance = models.CharField(max_length=100)
    # year = models.CharField(max_length=100)
 
    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "Unsold bill"
        verbose_name_plural = "Unsold bills"
        db_table = "V_UNSOLD_BILLS"
        
class HandoverDetailReport(models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    CODE = models.CharField(max_length=100)
    KEBELE = models.CharField(max_length=100)
    ZONE = models.CharField(max_length=100)
    SERVICE = models.CharField(max_length=100)
    CONSUMPTION = models.CharField(max_length=100)
    TOTAL_PRICE = models.CharField(max_length=100)
    MONTH = models.CharField(max_length=100)
    YEAR = models.CharField(max_length=100)

    def __str__(self):
        return self.CODE
    class Meta:
        managed = False
        verbose_name = "የቢል መረካከቢያ ዝርዝር ሪፖርት"
        verbose_name_plural="የቢል መረካከቢያ ዝርዝር ሪፖርት"
        db_table = "HANDOVER_DETAILS_REPORT"
        
class HandoverSummaryReport(models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    kebele = models.CharField(max_length=100)
    customer_total = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    total_consumption = models.CharField(max_length=100)
    total_bills = models.CharField(max_length=100)
    total_rent = models.CharField(max_length=100)
    total_price = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)

    def __str__(self):
        return self.service_type
    
    class Meta:
        managed = False
        verbose_name = "የቢል መረካከቢያ አጠቃላይ ሪፖርት"
        verbose_name_plural="የቢል መረካከቢያ አጠቃላይ ሪፖርት"
        db_table = "HANDOVER_SUMMARY_REPORT"


class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    bill_id = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    kebele = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    service = models.CharField(max_length=250)
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=25, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(null=True, blank=True)
    bank_transaction_reference = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    month = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)

    class Meta:
        managed = False  # Since this is a view, Django shouldn't manage migrations
        db_table = "payment_method"  # Must match the name of your SQL view

    def __str__(self):
        return f"{self.code} - {self.payment_method}"
    
class BankBalance(models.Model):
    id = models.AutoField(primary_key=True)  # Now matches the view's ID
    bank_name = models.CharField(max_length=100)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "bank_balance"

    def __str__(self):
        return f"{self.bank_name}: {self.total_balance}"
    
class PaymentSummaryPeriod(models.Model):
    id = models.IntegerField(primary_key=True)
    service_type = models.CharField(max_length=250)
    transaction_count = models.IntegerField()
    bill_price = models.DecimalField(max_digits=12, decimal_places=2)
    guage_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=10)

    class Meta:
        managed = False  # This is a database view
        db_table = 'payment_summary_period'  # Make sure it matches your actual view name
        verbose_name = "Sold Bills by Service Types Summary"
        verbose_name_plural = "Sold Bills by Service Types Summaries"

    def __str__(self):
        return f"{self.service_type} | {self.month}-{self.year}"
    
class UnsoldPaymentSummaryPeriod(models.Model):
    id = models.IntegerField(primary_key=True)
    service_type = models.CharField(max_length=250)
    customer_count = models.IntegerField()
    bill_price = models.DecimalField(max_digits=12, decimal_places=2)
    guage_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=10)

    class Meta:
        managed = False  # This is a database view
        db_table = 'unsold_payment_summary_period'  # Make sure it matches your actual view name
        verbose_name = "UnSold Bills by Service Types Summary"
        verbose_name_plural = "UnSold Bills by Service Types Summaries"

    def __str__(self):
        return f"{self.service_type} | {self.month}-{self.year}"

class CombinedBalanceSummary(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField()
    year = models.IntegerField()
    total_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_sold_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_unsold_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2)
    total_sold_bill = models.DecimalField(max_digits=10, decimal_places=2)
    total_unsold_bill = models.DecimalField(max_digits=10, decimal_places=2)
    sold_transaction_count = models.IntegerField()
    unsold_customer_count = models.IntegerField()

    class Meta:
        managed = False  # This tells Django not to manage the table creation
        db_table = 'combined_balance_summary'  # Your view name
        verbose_name = 'Combined Balance Summary'
        verbose_name_plural = 'Combined Balance Summaries'
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.month}/{self.year} - Sold: {self.total_sold_bill}, Unsold: {self.total_unsold_bill}"
    
class CombinedBalanceSummaryByService(models.Model):
    id = models.AutoField(primary_key=True)
    service_type = models.CharField(max_length=100)
    month = models.CharField(max_length=27)
    year = models.IntegerField()
    total_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_sold_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_unsold_rent = models.DecimalField(max_digits=12, decimal_places=2)
    total_bill = models.DecimalField(max_digits=12, decimal_places=2)
    total_sold_bill = models.DecimalField(max_digits=12, decimal_places=2)
    total_unsold_bill = models.DecimalField(max_digits=12, decimal_places=2)
    sold_transaction_count = models.IntegerField()
    unsold_customer_count = models.IntegerField()

    class Meta:
        managed = False  # Since it's a database view
        db_table = 'combined_balance_summary_by_service'
        verbose_name = 'Service Balance Summary'
        verbose_name_plural = 'Service Balance Summaries'
        ordering = ['-year', '-month', 'service_type']

    def __str__(self):
        return f"{self.service_type} - {self.month}/{self.year}"