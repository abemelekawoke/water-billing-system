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

class VaultControl(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Date = models.DateField('ቀን')
    Turned_total = models.DecimalField('የዞረ', max_digits = 9, decimal_places = 2, default=0)
    Income = models.DecimalField('ገቢ', max_digits = 9, decimal_places = 2, default=0)
    Total_income = models.DecimalField('ጠቅላላ ገቢ', max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    Cost = models.DecimalField('ወጪ', max_digits = 9, decimal_places = 2, default=0)
    Balance = models.DecimalField('ከወጪ ቀሪ', max_digits = 9, decimal_places = 2, blank=True, null=True, default=0)
    
    Remark = models.CharField('ምርመራ', max_length = 150, blank=True)
    Registered_at = models.DateTimeField(auto_now=True, verbose_name="Registered at")
    Updated_by = CurrentUserField(related_name="ur1")
    Registered_by = CurrentUserField(related_name="rr1")
 
    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Vault Control"
        verbose_name_plural="Vault Controls"

    def save(self, *args, **kwargs):
        try:
            previous_balance = VaultControl.objects.latest('id').Balance
        except ObjectDoesNotExist:
            # If no BankBook records exist, set previous_balance to 0
            previous_balance = 0

        # Ensure previous_balance is not None
        if previous_balance is None:    
            previous_balance = 0

        # Update balance based on previous balance, deposite, and withdrawal
        self.Turned_total = previous_balance
        self.Total_income = self.Turned_total + self.Income
        self.Balance = previous_balance + self.Income - self.Cost

        super(VaultControl, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.Total_income = self.Turned_total + self.Income
    #     self.Balance = self.Total_income - self.Cost
    #     super(VaultControl, self).save(*args, **kwargs)