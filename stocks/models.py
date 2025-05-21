from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
from django.db import models
from django.utils import timezone
import datetime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.urls import reverse
from django.http import HttpResponse
from setups.models import *

class StockManagement(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Name = models.ForeignKey(ItemLists, on_delete=models.CASCADE)
    Measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField()
    Individual_price = models.DecimalField(max_digits = 11, decimal_places = 2)
    Total_price = models.DecimalField(max_digits = 11, decimal_places = 2)
    Material_status = models.BooleanField(default = True)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by5")
    Registered_by = CurrentUserField(related_name="pl_by5")

    def __str__(self):
        return "%s" % (self.Name.name)

    class Meta:
        verbose_name="Stock"
        verbose_name_plural="Stocks"

    def save(self, *args, **kwargs):
        self.Total_price = self.Quantity * self.Individual_price
        super(StockManagement, self).save(*args, **kwargs)
        
class MaterialSaleReport(models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    NAME = models.CharField(max_length=100)
    QUANTITY = models.CharField(max_length=100)
    SINGLE_PRICE = models.CharField(max_length=100)
    TOTAL_PRICE = models.CharField(max_length=100)
    MONTH_AMHARIC = models.CharField(max_length=100)
    MONTH_ENGLISH = models.CharField(max_length=100)
    YEAR = models.CharField(max_length=100)

    def __str__(self):
        return self.NAME
    class Meta:
        managed = False
        verbose_name = "ከዕቃ ሽያጭ ገቢ ዕለታዊ ሪፖርት"
        verbose_name_plural="ከዕቃ ሽያጭ ገቢ ዕለታዊ ሪፖርት"
        db_table = "MATERIALSALEREVENUEREPORT"
