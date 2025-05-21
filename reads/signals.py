# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.exceptions import ValidationError
# from reads.models import WaterRead, Schedule

# @receiver(pre_save, sender=WaterRead)
# def check_duplicate_water_read(sender, instance, **kwargs):
#     """Check for duplicate records and assign the latest schedule before saving."""

#     # Assign the latest schedule to WaterRead
#     latest_schedule = Schedule.objects.order_by('-id').first()
#     if latest_schedule:
#         instance.schedule = latest_schedule  # Assign the schedule instance

#     # Prevent duplicate entries (same code, month, and year)
#     existing_record = WaterRead.objects.filter(code=instance.code, month=instance.month, year=instance.year).first()
#     if existing_record:
#         raise ValidationError(
#             f"A water reading record for Code '{instance.code}', Month '{instance.month}', "
#             f"and Year '{instance.year}' already exists. Please update the existing record instead."
#         )
