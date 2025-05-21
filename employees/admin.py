from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection
from django.http import HttpResponse
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ExportMixin


class ExperienceInlineAdmin(admin.TabularInline):
    model = Experience
    extra = 1
    readonly_fields = ['id', 'net_duration']

class StaffAdmin(ImportExportModelAdmin):
    inlines = [ExperienceInlineAdmin]
    list_display = ("department", "first_name", "father_name", "last_name", 'gender', "print_employee_experience", "position", "colored_status", "hired_date", "registered_at")
    list_filter = ("department", "employee_status", "marital_status", "position", "hired_date")  # Sidebar filters
    list_display_links = ("department", "first_name", "father_name", "last_name", 'gender', "print_employee_experience", "position", "hired_date", "registered_at")
    search_fields = ("first_name", "father_name", "last_name", "position", "contact_number")
    ordering = ("-registered_at",)  # Show newest first
    
    readonly_fields = ("registered_at", "updated_at", "updated_by", "registered_by")  # Prevent manual edits
    
    fieldsets = (
        ("Personal Information", {
            "fields": ("first_name", "father_name", "last_name", 'gender', "date_of_birth", "marital_status", "contact_number"),
            "classes": ("wide",),  # CSS class for spacing
        }),
        ("Employment Details", {
            "fields": ("department", "position", "employee_status", "hired_date"),
        }),
        ("Education", {
            "fields": ("educational_level", "field_of_study", "completed_date"),
            "classes": ("collapse",),  # Collapsible section
        }),
        ("Tracking Information", {
            "fields": ("registered_at", "updated_at", "registered_by", "updated_by"),
            "classes": ("collapse",),  # Hide unnecessary fields
        }),
    )

    def print_employee_experience(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Print</a>',
            reverse('print_employee_experience', args=[obj.pk])
        )

    print_employee_experience.short_description = "Print"
    
    def colored_status(self, obj):
        """Highlight Employee Status in colors"""
        colors = {
            "active": "green",
            "inactive": "gray",
            "terminated": "red",
            "retired": "blue"
        }
        return format_html('<span style="color: {};">{}</span>', colors.get(obj.employee_status, "black"), obj.employee_status)
    
    colored_status.admin_order_field = "employee_status"
    colored_status.short_description = "Status"

    class Meta:
        model = StaffProfile

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.registered_at = datetime.now()
        obj.save()

    # class Media:
    #     css = {
    #         'all': ('css/admin_custom.css',)  # Path to your custom CSS file
    #     }

admin.site.register(StaffProfile, StaffAdmin)

# Define the resource class for exporting data
class EmployeePerformanceResource(resources.ModelResource):
    class Meta:
        model = EmployeePerformance
        fields = ("staff__first_name", "staff__father_name", "staff__last_name", 
                  "staff__department__name", "month", "year", "score", "rank")
        export_order = ("staff__first_name", "staff__father_name", "staff__last_name", 
                        "staff__department__name", "month", "year", "score", "rank")

# Extend ExportMixin for CSV and Excel export functionality
@admin.register(EmployeePerformance)
class EmployeePerformanceAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EmployeePerformanceResource  # Enables export
    list_display = ("staff", "staff_department", "month", "year", "colored_score", "colored_rank", "performance_status")
    list_filter = ("year", "month", "staff__department")
    search_fields = ("staff__first_name", "staff__father_name", "staff__last_name", "staff__department")
    ordering = ("-year", "-month", "-score", "rank")  # Order by score, then rank
    readonly_fields = ("year", "month", "rank")  
    list_per_page = 25  

    fieldsets = (
        ("Employee Details", {
            "fields": ("staff", "month", "year"),
            "classes": ("wide",),
        }),
        ("Performance Details", {
            "fields": ("score", "rank"),
            "classes": ("collapse",),
        }),
    )

    def staff_department(self, obj):
        """Display the department name of the staff"""
        return obj.staff.department.name if obj.staff.department else "N/A"
    staff_department.short_description = "Department"
    
    def colored_score(self, obj):
        """Color-code scores for visual clarity"""
        if obj.score >= 90:
            color = "green"
        elif obj.score >= 70:
            color = "orange"
        else:
            color = "red"
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.score}</span>')
    colored_score.admin_order_field = "score"
    colored_score.short_description = "Performance Score"

    def colored_rank(self, obj):
        """Highlight ranks with color"""
        color = "blue" if obj.rank == 1 else "black"
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.rank}</span>')
    colored_rank.admin_order_field = "rank"
    colored_rank.short_description = "Rank"

    def performance_status(self, obj):
        """Display performance level based on score"""
        if obj.score >= 90:
            return "🌟 Excellent"
        elif obj.score >= 70:
            return "✅ Good"
        else:
            return "⚠️ Needs Improvement"
    performance_status.short_description = "Status"

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'print_leave_request', 'start_date', 'end_date', 'status', 'created_at', 'updated_at')
    list_filter = ('leave_type', 'status', 'created_at')
    search_fields = ('employee__First_name', 'employee__Last_name', 'leave_type', 'reason')
    list_display_links = ['employee', 'leave_type', 'print_leave_request', 'start_date', 'end_date', 'status']
    ordering = ('-created_at',)  # Order by created_at descending
    
    def print_leave_request(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Print</a>',
            reverse('print_leave_request', args=[obj.pk])
        )

    print_leave_request.short_description = "Print"

    def has_change_permission(self, request, obj=None):
        # Custom permission logic if needed
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Custom permission logic if needed
        return super().has_delete_permission(request, obj)

# Register the model with the admin site
admin.site.register(LeaveRequest, LeaveRequestAdmin)

class MotorHomeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'schedule_date', 'motor_on_time', 'motor_off_time', 'created_at')
    list_filter = ('schedule_date', 'motor_on_time', 'motor_off_time')
    search_fields = ('employee__username',)
    readonly_fields = ('created_at',)
    ordering = ('schedule_date', 'motor_on_time')

    actions = ['mark_motor_on', 'mark_motor_off']

    @admin.action(description="Mark selected records as Motor On")
    def mark_motor_on(self, request, queryset):
        queryset.update(motor_on_time=now())

    @admin.action(description="Mark selected records as Motor Off")
    def mark_motor_off(self, request, queryset):
        queryset.update(motor_off_time=now())

admin.site.register(MotorHome, MotorHomeAdmin)

