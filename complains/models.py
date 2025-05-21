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
# Create your models here.
class ComplainManagement(models.Model):
    THEME_CHOICES1 = (
        ('1', 'First type'),
        ('2', 'Second type'),
        ('3', 'Third type'),
        ('4', 'Forth type'),
    )
    THEME_CHOICES2 = (
        ('1', 'First type'),
        ('2', 'Second type'),
        ('3', 'Third type'),
        ('4', 'Forth type'),
    )
    THEME_CHOICES3 = (
        ('1', 'First type'),
        ('2', 'Second type'),
        ('3', 'Third type'),
        ('4', 'Forth type'),
    )
    id = models.AutoField(primary_key = True, unique = True)
    Category = models.CharField(max_length = 150, choices = THEME_CHOICES1)
    Sub_category = models.CharField(max_length = 150, choices = THEME_CHOICES2)
    Complain_type = models.CharField(max_length = 150, choices = THEME_CHOICES3)
    Nature_of_complaint = models.CharField(max_length = 150)
    Complain_details = models.TextField(max_length = 250)
    Complain_related = models.FileField(upload_to='documents/%Y/%m/%d', max_length=254)
    Complained_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="z1")
    Registered_by = CurrentUserField(related_name="z2")

    def __str__(self):
        return "%s" % (self.id)
    class Meta:
        verbose_name="Complain management system"
        verbose_name_plural="Complain management systems"