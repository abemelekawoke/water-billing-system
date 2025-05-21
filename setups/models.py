from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
    
class Organization(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Organizations"

	def __str__(self):
		return "%s" % self.name

class Department(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Departments"

	def __str__(self):
		return "%s" % self.name

class Task(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Tasks"

	def __str__(self):
		return "%s" % self.name

class Measurement(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    value = models.PositiveIntegerField()
    
    class Meta:
        verbose_name_plural = "Measurements"

    def __str__(self):
        return "%s" % self.name
    
class ItemLists(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, unique=True)    
    description = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Item lists"

    def __str__(self):
        return "%s" % self.name

class Month(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	month_amharic = models.CharField(max_length=100, unique=True)
	month_english = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=250)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Months"
		abstract = False

	def __str__(self):
		return "%s" % self.month_english

class Year(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	year = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Years"
		abstract = False

	def __str__(self):
		return "%s" % self.year
   
class Reader(models.Model):
    """Reader model to represent users with assigned reading roles"""
    STATUS_CHOICES = (
		('Active', 'Active'),
		('Inactive', 'Inactive'),  # Corrected 'In Active' to 'Inactive'
	)
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)  # To store the username
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    def save(self, *args, **kwargs):
        # Automatically set the username before saving
        if self.user:
            self.name = self.user.username
        super(Reader, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name  # This will display the saved username
    
class Zone(models.Model):
    """Zone model to represent a geographical area with an assigned reader"""
    STATUS_CHOICES = (
		('Active', 'Active'),
		('Inactive', 'Inactive'),  # Corrected 'In Active' to 'Inactive'
	)
    id = models.AutoField(primary_key=True)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    zone = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"
        
    def __str__(self):
        return self.zone
		
class Kebele(models.Model):
	status = (
        ('Active', 'Active'),
        ('In Active', 'In Active'),
    )
	id = models.AutoField(primary_key=True, unique=True)
	kebele = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	def __str__(self):
	    return "%s" % self.kebele

class GaugeWidth(models.Model):
	status = (
        ('Active', 'Active'),
        ('In Active', 'In Active'),
    )
	id = models.AutoField(primary_key=True, unique=True)
	width = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	def __str__(self):
	    return "%s" % self.width

class ServiceType(models.Model):
	status = (
        ('Active', 'Active'),
        ('In Active', 'In Active'),
    )
	id = models.AutoField(primary_key=True, unique=True)
	service = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	def __str__(self):
	    return "%s" % self.service
 
class Service(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(max_length=100, unique=True)  
	description = models.CharField(max_length=250, blank=True, null=True)
	status = models.CharField(max_length=50, choices=status, default='Active')

	def __str__(self):
		return "%s" % self.name

class ServiceCharge(models.Model):
	status = (
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	status = models.CharField(max_length=50, choices=status, default='Active')

	def __str__(self):
		return "%s" % self.id

class Block(models.Model):
	status=(
		('Active', 'Active'),
		('In Active', 'In Active'),
	)
	id = models.AutoField(primary_key=True, unique=True)
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	value = models.PositiveIntegerField()
	status = models.CharField(max_length=150, choices=status, default='Active')

	def __str__(self):
		return self.name
		
class Tariff(models.Model):
	"""docstring for Tariff"""
	status = (
        ('Active', 'Active'),
        ('In Active', 'In Active'),
    )
	id = models.AutoField(primary_key=True, unique=True)
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	min_consumption = models.PositiveBigIntegerField(default=0)
	max_consumption = models.PositiveBigIntegerField(default=0)
	block1 = models.PositiveBigIntegerField(default=0)
	block2 = models.PositiveBigIntegerField(default=0)
	block3 = models.PositiveBigIntegerField(default=0)
	block4 = models.PositiveBigIntegerField(default=0)
	block5 = models.PositiveBigIntegerField(default=0)

	status = models.CharField(max_length=150, choices=status, default='Active')

	def __str__(self):
		return self.service_type.service
		
class Penalty(models.Model):
	"""docstring for Tariff"""
	status = (
        ('Active', 'Active'),
        ('In Active', 'In Active'),
    )
	id = models.AutoField(primary_key=True, unique=True)
	service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	# months = models.PositiveIntegerField()
	penalty = models.PositiveIntegerField()
	status = models.CharField(max_length=150, choices=status, default='Active')

	class Meta:
		verbose_name_plural = "Penalities"

	def __str__(self):
		return "%s" % self.name
