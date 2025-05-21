from django.conf import settings
from django.db import models
from setups.models import *

class Season(models.Model):
	"""docstring for ItemBalance"""
	MONTH_ID = models.AutoField(primary_key=True)
	MONTH_AMHARIC = models.CharField(max_length=50)
	MONTH_ENGLISH = models.CharField(max_length=50)
	YEAR_ID = models.CharField(max_length=50)
	YEAR = models.CharField(max_length=50)
	
	def __str__(self):
		return "%s" % self.MONTH_AMHARIC

	class Meta:
		managed=False
		db_table='ACTIVE_SEASON'
		# order_by=self.mid

class InputDataCurrentSeason(models.Model):
    
	def get_current_month_id():
		try:
			current_month = Month.objects.get(status__iexact='Active')
			return current_month.id
		except Month.DoesNotExist:
			return None
		
	def get_current_month():
		try:
			current_month = Month.objects.get(status__iexact='Active')
			return current_month
		except Month.DoesNotExist:
			return None
		
	def get_current_year_id():
		try:
			current_year = Year.objects.get(status__iexact='Active')
			return current_year.id
		except Year.DoesNotExist:
			return None

	def get_current_year():
		try:
			current_year = Year.objects.get(status__iexact='Active')
			return current_year
		except Year.DoesNotExist:
			return None
        
	mid = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='smonthid', default=get_current_month_id)
	month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='smonth', default=get_current_month)
	yid = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='syearid', default=get_current_year_id)
	year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='syear', default=get_current_year)

	def __str__(self):
		return f"Month: {self.month}, Year: {self.year}"

	class Meta:
		verbose_name = "Season change"
		verbose_name_plural = "Season changes"