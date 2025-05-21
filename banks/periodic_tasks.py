# from celery.schedules import crontab
# from django_celery_beat.models import PeriodicTask, CrontabSchedule
# import json

# def create_periodic_task():
#     """
#     Creates a periodic task to run the bill sync task automatically every day at 6 PM.
#     """
#     # Define a crontab schedule (Runs at 6:00 PM every day)
#     schedule, created = CrontabSchedule.objects.get_or_create(
#         minute=0,
#         hour=18,  # 6 PM (24-hour format)
#         day_of_week="*",  # Every day
#         day_of_month="*",  # Every day of the month
#         month_of_year="*",  # Every month
#     )

#     # Define the task if it doesn't already exist
#     task_name = "sync_bills_task"
#     if not PeriodicTask.objects.filter(name=task_name).exists():
#         PeriodicTask.objects.create(
#             crontab=schedule,  # Use crontab instead of interval
#             name=task_name,
#             task="banks.tasks.sync_bills_task",
#             args=json.dumps([]),  # Empty list, pass dynamic args in the task
#         )
#         print(f"Periodic task '{task_name}' created successfully to run every day at 6 PM.")
#     else:
#         print(f"Periodic task '{task_name}' already exists.")
