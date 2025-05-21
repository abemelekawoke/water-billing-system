from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from setups.models import *
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Client(models.Model):
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
        
	Gender_choices = (
	    ('Male', 'Male'),
	    ('Female', 'Female'),
	)
	Marital_choices = (
	    ('Single', 'Single'),
	    ('Married ', 'Married'),
	)
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
		('Transferred', 'Transferred'),
		('Disconnected', 'Disconnected'),
	)
	id = models.AutoField(primary_key = True, unique = True)
	amharic_full_name = models.CharField('ሙሉ ስም', max_length=100)
	# amharic_father_name = models.CharField('የአባት ስም', max_length=100)
	# amharic_last_name = models.CharField('የአያት ስም', max_length=100)

	english_full_name = models.CharField('Full name', max_length=100)
	# english_father_name = models.CharField('Father name', max_length=100)
	# english_last_name = models.CharField('Last name', max_length=100)

	gender = models.CharField(max_length=100, choices=Gender_choices, null=True, blank=True)
	marital_status = models.CharField(max_length=100, choices=Marital_choices, null=True, blank=True)
	# reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reader', blank=True, null=True)

	contact_number = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
	destrict = models.CharField(max_length=100, default='South Achefer')
	kebele = models.ForeignKey(Kebele, on_delete=models.CASCADE)
	place_name = models.CharField(max_length=100, null=True, blank=True)
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	house_number = models.CharField(max_length=100, null=True, blank=True)

	code = models.CharField(max_length=100, unique=True, default='DRB-')
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	guage_width = models.ForeignKey(GaugeWidth, on_delete=models.CASCADE)
	month = models.CharField(max_length=50, default=get_current_month)
	year = models.CharField(max_length=50, default=get_current_year) 
	initial_read = models.CharField(max_length=100, default=0)
	first_read = models.CharField(max_length=100, default=0)
	deposit = models.PositiveBigIntegerField(null=True, blank=True)
	read_date = models.CharField(max_length=100, null=True, blank=True)
	contract_number = models.CharField(max_length=100, null=True, blank=True)
	contract_file = models.FileField(upload_to='contracts/', null=True, blank=True)
	customer_image = models.ImageField(upload_to='customer_images/', null=True, blank=True)
	customer_status = models.CharField(max_length=50, choices=status, default='Active')

	created_by = CurrentUserField(related_name="c1")
	created_at = models.DateField(auto_now=True)
	modified_by = CurrentUserField(related_name="m1")
	modified_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"{self.amharic_full_name} {self.code} {self.zone}"

class CounterNumber(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="counters")
    counter_number = models.CharField(max_length=50, unique=True)
    date_changed = models.DateField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)

    def __str__(self):
        return f"{self.counter_number} {self.date_changed} ({self.status})"
	
class RenewContract(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	full_name = models.CharField(max_length=100)
	gender = models.CharField(max_length=100)
	contact_number = models.CharField(max_length=100)
	code = models.CharField(max_length=25)
	kebele = models.CharField(max_length=25)

	place_name = models.CharField(max_length=100)
	zone = models.CharField(max_length=30)
	house_number = models.CharField(max_length=100)
	service_type = models.CharField(max_length=30)
	guage_width = models.CharField(max_length=30)

	month = models.CharField(max_length=50)
	year = models.CharField(max_length=50) 
	customer_status = models.CharField(max_length=50)
	created_at = models.CharField(max_length=50)
	number_of_years = models.CharField(max_length=50)

	def __str__(self):
		return "%s" % self.full_name
    
	class Meta:
			managed = False
			verbose_name = "በየሁለት አመቱ ውል የሚታደስላቸው ደንበኞች"
			verbose_name_plural = "በየሁለት አመቱ ውል የሚታደስላቸው ደንበኞች ዝርዝር"
			db_table = "RENEW_CONTRACT_CUSTOMERS"
   
class ConsiderationFree(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	full_name = models.CharField(max_length=100)
	gender = models.CharField(max_length=100)
	contact_number = models.CharField(max_length=100)
	code = models.CharField(max_length=25)
	kebele = models.CharField(max_length=25)

	place_name = models.CharField(max_length=100)
	zone = models.CharField(max_length=30)
	house_number = models.CharField(max_length=100)
	service_type = models.CharField(max_length=30)
	guage_width = models.CharField(max_length=30)

	month = models.CharField(max_length=50)
	year = models.CharField(max_length=50) 
	customer_status = models.CharField(max_length=50)
	created_at = models.CharField(max_length=50)
	number_of_years = models.CharField(max_length=50)

	def __str__(self):
		return "%s" % self.full_name
    
	class Meta:
			managed = False
			verbose_name = "ከጋራ ግምት ክፍያ ውጪ የሆኑ ደንበኞች"
			verbose_name_plural = "ከጋራ ግምት ክፍያ ውጪ የሆኑ ደንበኞች ዝርዝር"
			db_table = "CONSIDERATION_FREE_CUSTOMERS"
   
class Clearance(models.Model):
	id = models.AutoField(primary_key = True, unique = True)
	code = models.CharField(max_length=25)
	full_name = models.CharField(max_length=100)
	gender = models.CharField(max_length=100)
	contact_number = models.CharField(max_length=100)
	deposit = models.CharField(max_length=50)
	total_bill = models.CharField(max_length=50) 
	balance = models.CharField(max_length=50)
	
	def __str__(self):
		return "%s" % self.full_name
    
	class Meta:
			managed = False
			verbose_name = "Clearance"
			verbose_name_plural = "Clearances"
			db_table = "CLEARANCE"