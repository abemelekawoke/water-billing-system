from operator import truediv
from turtle import mode
from django.db import models
from setups.models import *
from customers.models import *

from django.db import IntegrityError
from django.core.exceptions import ValidationError
class Schedule(models.Model):
    
    STATUS_CHOICES = [
        ('ON', 'ON'),
        ('OFF', 'OFF'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    
class InputDataSheet(models.Model):
    def get_current_month():
        try:
            current_month = Month.objects.get(status__iexact='Active')
            month = current_month.month_english
            return month
        except Month.DoesNotExist:
            return None

    def get_current_year():
        try:
            current_year = Year.objects.get(status__iexact='Active')
            year = current_year.year
            return year
        except Year.DoesNotExist:
            return None
        
    month = models.CharField(max_length=50, default=get_current_month)
    year = models.CharField(max_length=50, default=get_current_year)

    def __str__(self):
        return f"Month: {self.month}, Year: {self.year}"
    
    class Meta:
        verbose_name = "Prepare sheet"
        verbose_name_plural = "Prepare sheets"
    
class WaterRead(models.Model):
    def get_current_month():
        try:
            current_month = Month.objects.get(status__iexact='Active')
            month = current_month.month_english
            return month
        except Month.DoesNotExist:
            return None

    def get_current_year():
        try:
            current_year = Year.objects.get(status__iexact='Active')
            year = current_year.year
            return year
        except Year.DoesNotExist:
            return None

    id = models.AutoField(primary_key = True, unique = True)
    code = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='zones')
    month = models.CharField(max_length=50, default=get_current_month)
    year = models.CharField(max_length=50, default=get_current_year) 
    previous_read = models.BigIntegerField(help_text="ያለፈው ወር ንባብ")	
    current_read = models.BigIntegerField(help_text="የዚህ ወር ንባብ", null=True, blank=True)
    consumption = models.BigIntegerField(help_text="የዚህ ወር ፍጆታ", null=True, blank=True)
    next_my = models.PositiveIntegerField('Season flag', default=0)
    schedule = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Customer code: {self.code}"
    
    class Meta:
        ordering = ['-id']
        # abstract = True
        # constraints = [
        #     models.UniqueConstraint(fields=['code', 'zone', 'month', 'year', 'previous_read', 'current_read', 'consumption', 'next_my', 'schedule'], name='unique_water_read')
        # ]
    
    def save(self, *args, **kwargs):
        # Optional: update schedule status
        latest_schedule = Schedule.objects.order_by('-id').first()
        if latest_schedule:
            self.schedule = latest_schedule.status

        # Calculate consumption
        if self.current_read is not None and self.previous_read is not None:
            self.consumption = self.current_read - self.previous_read
        else:
            self.consumption = 0

        super().save(*args, **kwargs)
        
class ConsumptionZeroCount(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    code = models.CharField(max_length=100)
    consecutive_zero_count = models.CharField(max_length=50)
    year = models.CharField(max_length=50) 
    
    def has_change_permission(self, request, obj=None):
        return False
    
    
    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "Consumptions zero count"
        verbose_name_plural = "Consumptions zero counts"
        db_table = "v_consumptions_zero_count"

class ReaderComparison(models.Model):
    # id = models.AutoField(primary_key = True, unique = True)
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    readings_count = models.CharField(max_length=100)
    total_consumption = models.CharField(max_length=100)
    discrepancies = models.CharField(max_length=100)
    rank_by_readings = models.CharField(max_length=100)

    class Meta:
        managed = False  # This is a database view, not a Django-managed table
        db_table = "reader_comparison"  # Matches the name of the database view
        verbose_name = "Reader comparison"
        verbose_name_plural = "Reader comparisons"

    def __str__(self):
        return f"Name {self.name} - Zone {self.zone} - Rank {self.rank_by_readings}"