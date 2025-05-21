from import_export import resources
from django.db.models import Subquery, OuterRef
from django.db import connection
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
from django.utils.timezone import now
from datetime import date

# Create your models here.
from django.db import models, transaction
import django_currentuser.db.models.fields
from django.conf import settings
import django.db.models.deletion
from setups.models import *
class StaffProfile(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    EMPLOYEE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('retired', 'Retired'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=150, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='single')
    contact_number = models.CharField(max_length=15)
    hired_date = models.DateField()  # Changed to DateField for proper date storage

    educational_level = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=200)
    completed_date = models.DateField()
    position = models.CharField(max_length=150)

    employee_status = models.CharField(max_length=10, choices=EMPLOYEE_STATUS_CHOICES, default='active')

    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Registered at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    updated_by = django_currentuser.db.models.fields.CurrentUserField(related_name="staff_updated_by")
    registered_by = django_currentuser.db.models.fields.CurrentUserField(related_name="staff_registered_by")

    def __str__(self):
        return f"{self.first_name} {self.father_name}"

    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"
        # db_table = 'staff_profile'  # Uncomment if you need a custom table name

class Experience(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="experiences")
    institution = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    position = models.CharField(max_length=150)
    net_duration = models.CharField(max_length=50, blank=True, null=True)  # Will be auto-calculated

    def save(self, *args, **kwargs):
        """Automatically calculate the net duration in years, months, and days"""
        if self.from_date and self.to_date:
            delta = self.to_date - self.from_date
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            self.net_duration = f"{years} years, {months} months, {days} days"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} - {self.position} at {self.institution}"

    class Meta:
        ordering = ["-to_date"]
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

class EmployeePerformance(models.Model):
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
    id = models.AutoField(primary_key=True, unique=True)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="performance_scores")
    month = models.CharField(max_length=50, default=get_current_month)
    year = models.CharField(max_length=50, default=get_current_year) 
    score = models.FloatField()
    rank = models.PositiveIntegerField(null=True, blank=True)  # Nullable initially

    class Meta:
        unique_together = ('staff', 'year')  # Prevent duplicate scores for the same year
        ordering = ['-score']  # Ensure ranking is based on score

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first
        self.update_ranking()  # Call ranking function

    @classmethod
    def update_ranking(cls):
        """
        Update ranks for all employees based on their scores in the same year.
        """
        with transaction.atomic():  # Ensure database consistency
            current_year = get_current_year()
            performances = list(cls.objects.filter(year=current_year).order_by('-score'))  # Order by highest score

            rank = 1
            for index, performance in enumerate(performances):
                if index > 0 and performance.score < performances[index - 1].score:
                    rank = index + 1  # Adjust rank if score is lower
                performance.rank = rank
                performance.save(update_fields=['rank'])  # Save only rank

    def __str__(self):
        return f"{self.staff.first_name} {self.staff.father_name} ({self.year}) - {self.score} - Rank: {self.rank}"

class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Vacation Leave', 'Vacation Leave'),
    ]
    
    Leave = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Leave, default='Pending')  # e.g., Pending, Approved, Rejected
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"
    
class MotorHome(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    employee = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="motorhome_entries")
    schedule_date = models.DateField(help_text="Scheduled date for the employee in the motor home queue.")
    motor_on_time = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the motor was turned on.")
    motor_off_time = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the motor was turned off.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp.")

    class Meta:
        ordering = ['schedule_date', 'motor_on_time']
    
    def __str__(self):
        return f"{self.employee.first_name} - Scheduled: {self.schedule_date} - Status: {'On' if self.motor_on_time and not self.motor_off_time else 'Off'}"
    
    def start_motor(self):
        """Set motor on time to the current time."""
        self.motor_on_time = now()
        self.save()

    def stop_motor(self):
        """Set motor off time to the current time."""
        self.motor_off_time = now()
        self.save()


