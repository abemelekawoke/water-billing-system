
# Register your models here.
from django.contrib import admin
from .models import Challenge

class ChallengeAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'incident_type', 'priority', 'status', 'reported_by', 'assigned_to', 'reported_on', 'updated_on')
    
    # Fields to search by in the admin interface
    search_fields = ('title', 'description', 'reported_by__username', 'assigned_to__username', 'location')
    
    # Filters in the admin sidebar
    list_filter = ('status', 'priority', 'incident_type', 'reported_on')
    
    # Fields that should be read-only in the admin interface
    readonly_fields = ('reported_on', 'updated_on', 'reported_by')
    
    # Fieldsets to organize the form layout in the admin detail view
    fieldsets = (
        ('Challenge Details', {
            'fields': [('title'), 'description', ('incident_type', 'priority'), ('status')]
        }),
        ('Reporter and Assignee', {
            'fields': [('reported_by', 'assigned_to')]
        }),
        ('Timestamps', {
            'fields': ('reported_on', 'updated_on')
        }),
        ('Additional Info', {
            'fields': ('location', 'supporting_documents', 'remarks')
        }),
    )

    # Setting up the default ordering in the admin view
    ordering = ('-reported_on',)
    
    # Automatically fill the 'reported_by' field with the current user
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new challenge being created
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)

# Register the model and the custom admin class
admin.site.register(Challenge, ChallengeAdmin)
