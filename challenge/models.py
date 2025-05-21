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

from django.contrib.auth.models import User

class Challenge(models.Model):
    REPORT_STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    INCIDENT_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('logistical', 'Logistical'),
        ('safety', 'Safety'),
        ('other', 'Other'),
    ]

    # General details of the challenge
    title = models.CharField(max_length=200, help_text="Brief title or subject of the challenge")
    description = models.TextField(help_text="Detailed description of the challenge")
    
    # Meta details of the challenge
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPE_CHOICES, default='other', help_text="Type of challenge or incident")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low', help_text="Priority level of the challenge")
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='new', help_text="Current status of the report")
    
    # Information on who reported it
    reported_by = CurrentUserField(related_name="reported_challenges", help_text="User who reported the challenge")
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_challenges", help_text="User assigned to resolve the challenge")
    
    # Timestamps
    reported_on = models.DateTimeField(default=timezone.now, help_text="When the challenge was reported")
    updated_on = models.DateTimeField(auto_now=True, help_text="When the challenge was last updated")
    
    # Location or area where the challenge occurred
    location = models.CharField(max_length=200, null=True, blank=True, help_text="Location of the challenge or incident")
    
    # Additional information
    supporting_documents = models.FileField(upload_to='challenges/documents/', null=True, blank=True, help_text="Any supporting documents related to the challenge")
    remarks = models.TextField(null=True, blank=True, help_text="Additional remarks or notes about the challenge")
    
    def __str__(self):
        return self.title
