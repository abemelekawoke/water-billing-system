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
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.utils.html import format_html
# from crum import get_current_request
# Create your models here.
class BankBook(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Date = models.DateField()
    Deposite = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Withdrawal = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Balance = models.DecimalField(max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="up_by44")
    Registered_by = CurrentUserField(related_name="pl_by44")

    def __str__(self):
        return "%s" % (self.id)

    def save(self, *args, **kwargs):
        try:
            previous_balance = BankBook.objects.latest('id').Balance
        except ObjectDoesNotExist:
            # If no BankBook records exist, set previous_balance to 0
            previous_balance = 0

        # Ensure previous_balance is not None
        if previous_balance is None:    
            previous_balance = 0

        # Update balance based on previous balance, deposite, and withdrawal
        self.Balance = previous_balance + self.Deposite - self.Withdrawal

        super(BankBook, self).save(*args, **kwargs)

class BankUpload(models.Model):
    """
    Model representing bills to be uploaded to the banking system.
    This model maps to a database view (managed=False) rather than a table.
    """
    index = models.IntegerField(
        primary_key=True,
        verbose_name="Index",
        help_text="Unique identifier for the record"
    )
    
    bill_id = models.TextField(
        verbose_name="Bill ID",
        help_text="Unique identifier for the bill",
        db_index=True
    )
    
    bill_description = models.CharField(
        max_length=255,
        verbose_name="Description",
        help_text="Description of the bill"
    )
    
    bill_reason = models.CharField(
        max_length=255,
        verbose_name="Reason",
        help_text="Reason for the bill generation"
    )
    
    amount_due = models.DecimalField(
        max_digits=25,
        decimal_places=2,
        verbose_name="Amount Due",
        help_text="Total amount due for payment",
        validators=[MinValueValidator(0)]
    )
    
    customer_id = models.CharField(
        max_length=255,
        verbose_name="Customer ID",
        help_text="Unique identifier for the customer",
        db_index=True
    )
    
    name = models.CharField(
        max_length=255,
        verbose_name="Customer Name",
        help_text="Full name of the customer"
    )
    
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Due Date",
        help_text="Date when payment is due"
    )
    
    mobile = models.CharField(
        max_length=100,
        verbose_name="Mobile Number",
        help_text="Customer's mobile phone number"
    )
    
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name="Email Address",
        help_text="Customer's email address"
    )

    month = models.CharField(
        max_length=100,
        verbose_name="Month",
        help_text="Period month"
    )

    year = models.CharField(
        max_length=100,
        verbose_name="Year",
        help_text="Period year"
    )
    
    Prev_Read = models.PositiveBigIntegerField(
        verbose_name="Previous Reading",
        help_text="Previous meter reading value"
    )
    
    Curr_Read = models.PositiveBigIntegerField(
        verbose_name="Current Reading",
        help_text="Current meter reading value"
    )
    
    Consumtion = models.PositiveBigIntegerField(
        verbose_name="Consumption",
        help_text="Calculated consumption value",
        # Note: Field name appears to have a typo (Consumtion vs Consumption)
    )

    class Meta:
        managed = False  # Indicates this model maps to a view, not a table
        db_table = 'bank_upload'  # The name of the view in the database
        ordering = ['-due_date']  # Default ordering by due date (newest first)

    def __str__(self):
        return f"{self.bill_id} - {self.name} - {self.amount_due}"
  
class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    valid_until = models.DateField()
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    customer_id = models.CharField(max_length=10)
    bill_id = models.CharField(max_length=20)
    status = models.CharField(max_length=20, blank=True, null=True, default='Pending')

    def __str__(self):
        return f"{self.full_name}"
    
    class Meta:
        verbose_name = 'Update single bill'
        verbose_name_plural = 'Update single bills'

class Item(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"
    
class BillSync(models.Model):
    start_date = models.DateField()
    max = models.IntegerField(null=True, blank=True, default=2147483647)
    end_date = models.DateField()
    status = models.CharField(max_length=20, blank=True, null=True, default='Pending')
    sync_date = models.DateTimeField(auto_now_add=True)
    # Fields for the returned data
    bill_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    paid_on = models.DateTimeField(blank=True, null=True)
    bank_transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Sync from {self.start_date} to {self.end_date}"
    
class BillSyncFile(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    downloaded_file = models.FileField(upload_to='sync_files/', blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending'
    )
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sync File: {self.start_date} to {self.end_date}"
    
class BillCancellation(models.Model):
    bill_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, null=True, blank=True, default='Pending')
    cancel_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill_id} - {self.status}"
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Cancel single bill'
        verbose_name_plural = 'Cancel single bills'
    
class BulkBillCancellation(models.Model):
    uploaded_file = models.FileField(upload_to='bulk_bill_cancellations/')
    status = models.CharField(max_length=20, null=True, blank=True, default='Pending')
    cancel_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bulk Cancellation - {self.cancel_date}"
    
class BulkBillUpload(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    file = models.FileField(upload_to='bulk_bill_uploads/', verbose_name="Bill File")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True, verbose_name="Error Details")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Upload Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return f"Upload #{self.id} ({self.get_status_display()})"

    def status_badge(self):
        color_map = {
            'pending': '#FF9800',  # orange
            'success': '#4CAF50',  # green
            'failed': '#F44336',   # red
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; '
            'border-radius: 12px; font-weight: bold; font-size: 12px; text-transform: uppercase;">{}</span>',
            color_map[self.status],
            self.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def file_link(self):
        if self.file:
            return format_html(
                '<a href="{}" download style="color: #2196F3; font-weight: 500;">{}</a>',
                self.file.url,
                self.file.name.split('/')[-1]
            )
        return "-"
    file_link.short_description = "File"

    class Meta:
        verbose_name = "Bulk Bill Upload"
        verbose_name_plural = "Bulk Bill Uploads"
        ordering = ['-created_at']