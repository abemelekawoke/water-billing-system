from django.db import models

# Create your models here.

class RevenuePerformanceFromJulyToSeptember(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Revenue_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.Revenue_title_amharic)

    class Meta:
        managed = False
        verbose_name = "የገቢ 1ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የገቢ 1ኛ ሩብ አመት ሪፖርት"
        db_table = "Revenue_from_July_to_September"

class RevenuePerformanceFromOctoberToDecember(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Revenue_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የገቢ 2ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የገቢ 2ኛ ሩብ አመት ሪፖርት"
        db_table = "REVENUE_FROM_OCTOBER_TO_DECEMBER"

class RevenuePerformanceFromJanuaryToMarch(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Revenue_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የገቢ 3ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የገቢ 3ኛ ሩብ አመት ሪፖርት"
        db_table = "Revenue_from_January_to_March"

class RevenuePerformanceFromAprilToJune(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Revenue_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የገቢ 4ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የገቢ 4ኛ ሩብ አመት ሪፖርት"
        db_table = "Revenue_from_April_to_June"

class RevenueMonthlyPerformance(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Month = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Revenue_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የገቢ ወራዊ ሪፖርት"
        verbose_name_plural = "የገቢ ወራዊ ሪፖርት"
        db_table = "Revenue_monthly_performance"

class RevenueAnnualPerformance(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Revenue_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Revenue_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የገቢ አመታዊ ሪፖርት"
        verbose_name_plural = "የገቢ አመታዊ ሪፖርት"
        db_table = "Revenue_annual_performance"

class ExpensePerformanceFromAprilToJune(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Expense_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የወጪ 4ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የወጪ 4ኛ ሩብ አመት ሪፖርት"
        db_table = "Expense_from_April_to_June"

class ExpensePerformanceFromJanuaryToMarch(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Expense_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የወጪ 3ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የወጪ 3ኛ ሩብ አመት ሪፖርት"
        db_table = "Expense_from_January_to_March"

class ExpensePerformanceFromJulyToSeptember(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Expense_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)
    
    class Meta:
        managed = False
        verbose_name = "የወጪ 1ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የወጪ 1ኛ ሩብ አመት ሪፖርት"
        db_table = "Expense_from_July_to_September"

class ExpensePerformanceFromOctoberToDecember(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Expense_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የወጪ 2ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የወጪ 2ኛ ሩብ አመት ሪፖርት"
        db_table = "Expense_from_October_to_December"

class ExpenseMonthlyPerformance(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Month = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Expense_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የወጪ ወራዊ ሪፖርት"
        verbose_name_plural = "የወጪ ወራዊ ሪፖርት"
        db_table = "Expense_monthly_performance"

class ExpenseAnnualPerformance(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Code = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Expense_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Expense_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የወጪ አመታዊ ሪፖርት"
        verbose_name_plural = "የወጪ አመታዊ ሪፖርት"
        db_table = "Expense_annual_performance"

# Potable water starts here
class PotableWaterPerformanceFromJulyToSeptember(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Year = models.CharField(max_length = 150)
    Service_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Service_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የመጠጥ ውሃ 1ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural = "የመጠጥ ውሃ 1ኛ ሩብ አመት ሪፖርት"
        db_table = "Potable_water_from_July_to_September"

class PotableWaterPerformanceFromOctoberToDecember(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Year = models.CharField(max_length = 150)
    Service_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Service_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የመጠጥ ውሃ 2ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural="የመጠጥ ውሃ 2ኛ ሩብ አመት ሪፖርት"
        db_table = "Potable_water_from_October_to_December"

class PotableWaterPerformanceFromJanuaryToMarch(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Year = models.CharField(max_length = 150)
    Service_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Service_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የመጠጥ ውሃ 3ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural="የመጠጥ ውሃ 3ኛ ሩብ አመት ሪፖርት"
        db_table = "Potable_water_from_January_to_March"

class PotableWaterPerformanceFromAprilToJune(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Year = models.CharField(max_length = 150)
    Service_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Service_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        managed = False
        verbose_name = "የመጠጥ ውሃ 4ኛ ሩብ አመት ሪፖርት"
        verbose_name_plural="የመጠጥ ውሃ 4ኛ ሩብ አመት ሪፖርት"
        db_table = "Potable_water_from_April_to_June"

class PotableWaterMonthlyPerformance(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Month = models.CharField(max_length = 150)
    Year = models.CharField(max_length = 150)
    Service_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Service_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Potable water performance"
        # verbose_name_plural="Expense performance" 
    class Meta:
        managed = False
        verbose_name = "የመጠጥ ውሃ ወራዊ ሪፖርት"
        verbose_name_plural="የመጠጥ ውሃ ወራዊ ሪፖርት"
        db_table = "Potable_water_monthly_performance"

class PotableWaterAnnualPerformance(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    Year = models.CharField(max_length = 150)
    Service_title_amharic = models.CharField(max_length = 150)
    Measurement = models.CharField(max_length = 150)
    Service_annual_plan = models.CharField(max_length = 150)
    Plan = models.CharField(max_length = 150)
    Performed = models.CharField(max_length = 150)
    Performance = models.CharField(max_length = 150)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name="Potable water annual performance"
        # verbose_name_plural="Expense performance" 
    class Meta:
        managed = False
        verbose_name = "የመጠጥ ውሃ አመታዊ ሪፖርት"
        verbose_name_plural="የመጠጥ ውሃ አመታዊ ሪፖርት"
        db_table = "Potable_water_annual_performance"