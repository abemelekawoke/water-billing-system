# employees/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin/leave-request/print/<int:pk>/', views.print_leave_request, name='print_leave_request'),
    path('employee/<int:employee_id>/experience/', views.print_employee_experience, name='print_employee_experience'),
]
