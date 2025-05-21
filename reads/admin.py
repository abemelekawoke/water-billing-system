from django.contrib import admin
from .models import *
from django.db import connection, transaction
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from setups.models import *
from periods.models import Season
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import RelatedOnlyFieldListFilter
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
# from dateutil.relativedelta import relativedelta

class ScheduleAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'description', 'status']
    list_display = ['id', 'name', 'status', 'description']
    search_fields = ['name']
    list_editable = ['status']
    list_filter = ['status']
    list_display_links = ['id', 'name', 'description']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    class Meta:
        model = Schedule

admin.site.register(Schedule, ScheduleAdmin)

class InputDataSheetAdmin(admin.ModelAdmin):
    actions = ['run_stored_procedure']

    @transaction.atomic
    def run_stored_procedure(self, request, queryset):
        try:
            for input_data in queryset:
                month = input_data.month
                year = input_data.year  # Adjust based on actual field name

                # Log the values for debugging
                self.message_user(request, f"Calling stored procedure with month={month}, year={year}", messages.INFO)

                # Check for None values
                if None in [month, year]:
                    self.message_user(request, f"Skipping {input_data} due to missing data.", messages.WARNING)
                    continue

                with connection.cursor() as cursor:
                    cursor.callproc('prepare_sheet', [month, year])

            self.message_user(request, "Reading sheet prepared successfully.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error: {str(e)}", messages.ERROR)

    run_stored_procedure.short_description = "Prepare sheets"

admin.site.register(InputDataSheet, InputDataSheetAdmin)

class ConsumptionFilter(admin.SimpleListFilter):
    title = 'Consumption'  # Displayed title in the admin sidebar
    parameter_name = 'consumption'  # Parameter used in URL query
    
    def lookups(self, request, model_admin):
        return (
            ('zero', 'Zero Reading'),
            ('negative', 'Negative Reading'),
            ('over_reading', 'Over Reading'),
            ('blank_reading', 'Blank Reading'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'zero':
            return queryset.filter(consumption=0)
        elif self.value() == 'negative':
            return queryset.filter(consumption__lt=0)
        elif self.value() == 'over_reading':
            return queryset.filter(consumption__gt=30)
        elif self.value() == 'blank_reading':
            return queryset.filter(Q(current_read__isnull=True))
class WaterReadForm(forms.ModelForm):
    class Meta:
        model = WaterRead
        fields = [
            "code",
            "zone",
            "month",
            "year",
            "previous_read",
            "current_read",
            "consumption",
            "next_my",
            "schedule",
        ]

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        zone = cleaned_data.get("zone")
        month = cleaned_data.get("month")
        year = cleaned_data.get("year")
        
        previous_read = cleaned_data.get("previous_read")
        current_read = cleaned_data.get("current_read")
        # consumption = cleaned_data.get("consumption")
        next_my = cleaned_data.get("next_my")

        # Prevent duplicate records when adding a new record
        if self.instance.pk is None:  # This ensures check runs only on new additions
            if WaterRead.objects.filter(code=code, zone=zone, month=month, year=year, previous_read=previous_read, current_read=current_read, next_my=next_my).exists():
                raise ValidationError(
                    f"A water reading record for Code '{code}', Zone '{zone}', Month '{month}', and Year '{year}' already exists. Please update the existing record instead."
                )

        return cleaned_data
    
class WaterReadResource(resources.ModelResource):
    current_read = fields.Field()
    class Meta:
        model = WaterRead
        import_id_fields = ['id']
        exclude = ('id', 'previous_read', 'consumption', 'next_my', 'schedule')
        export_order = [
            'code', 'zone', 'month', 'year', 'current_read'
        ]

        def dehydrate_current_read(self, obj):
            return '' if obj.current_read == 0 else obj.current_read

        # import_id_fields = ['index']

class WaterReadAdmin(ImportExportModelAdmin):
    resource_class = WaterReadResource
    form = WaterReadForm  # Attach the custom form to admin
    fields = ['code', 'zone', 'month', 'year', 'previous_read', 'current_read', 'consumption', 'next_my']
    list_display = ['id', 'code', 'zone', 'month', 'year', 'previous_read', 'current_read', 'consumption', 'next_my']
    search_fields = ['code']
    list_editable = ['previous_read', 'current_read']
    list_filter = (ConsumptionFilter, 'zone__zone', 'month', 'year',)
    list_display_links = ['id', 'code', 'zone', 'month', 'year', 'consumption', 'next_my']
    readonly_fields = ('id', 'consumption',)
    list_per_page = 10
    list_select_related = True
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:
            # Get latest schedule
            latest_schedule = Schedule.objects.order_by('-id').first()
            if latest_schedule:
                obj.schedule = latest_schedule.status

            # Calculate consumption
            if obj.current_read is not None and obj.previous_read is not None:
                obj.consumption = obj.current_read - obj.previous_read
            else:
                obj.consumption = 0

            obj.save()

        formset.save_m2m()
        
    def changelist_view(self, request, extra_context=None):
        """
        Force recalculating consumption even if the user doesn't change a row.
        """
        if request.method == 'POST':
            # Get all IDs shown on the current page
            ids = request.POST.getlist('_selected_action')
            if not ids:
                # Fallback to all displayed rows on the current page
                ids = [str(obj.pk) for obj in self.get_queryset(request)]

            for obj in WaterRead.objects.filter(pk__in=ids):
                latest_schedule = Schedule.objects.order_by('-id').first()
                if latest_schedule:
                    obj.schedule = latest_schedule.status

                if obj.current_read is not None and obj.previous_read is not None:
                    obj.consumption = obj.current_read - obj.previous_read
                else:
                    obj.consumption = 0

                obj.save()

        return super().changelist_view(request, extra_context)
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)  # Path to your custom CSS file
        }
    
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term includes a comparison operator
        if search_term:
            comparison_operator = None
            if '<=' in search_term:
                comparison_operator = '<='
            elif '>=' in search_term:
                comparison_operator = '>='
            elif '<' in search_term:
                comparison_operator = '<'
            elif '>' in search_term:
                comparison_operator = '>'
            elif '==' in search_term:
                comparison_operator = '=='

            # Extract the number from the search term
            if comparison_operator:
                try:
                    value = float(search_term.split(comparison_operator)[1].strip())
                except (ValueError, IndexError):
                    value = None
                
                if value is not None:
                    if comparison_operator == '<':
                        queryset = queryset.filter(consumption__lt=value)
                    elif comparison_operator == '<=':
                        queryset = queryset.filter(consumption__lte=value)
                    elif comparison_operator == '>':
                        queryset = queryset.filter(consumption__gt=value)
                    elif comparison_operator == '>=':
                        queryset = queryset.filter(consumption__gte=value)
                    elif comparison_operator == '==':
                        queryset = queryset.filter(consumption=value)

                search_term = ''  # Clear the search term to avoid default filtering
                
            queryset = self.model.objects.filter(code__exact=search_term)
            use_distinct = False
            return queryset, use_distinct
        
        return super().get_search_results(request, queryset, search_term)
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.schedule == 'OFF':
            return ['current_read']  # Make 'current' field read-only
        return []  # Editable if status is 'ON'
    
    def save_model(self, request, obj, form, change):
        # Check if schedule exists and its status is 'OFF'
        if obj.schedule and obj.schedule == 'OFF':  # Compare with schedule status
            # Prevent saving and display an error message
            self.message_user(request, "Cannot edit 'current read' when schedule status is OFF", level=messages.ERROR)
            return  # Stop the save operation and exit

        # Check if duplicate record exists for the same code, month, and year
        # if WaterRead.objects.filter(code=obj.code, month=obj.month, year=obj.year).exists():
        #     self.message_user(request, f"A water reading record for Code '{obj.code}', Month '{obj.month}', and Year '{obj.year}' already exists. Please update the existing record instead.", level=messages.ERROR)
        #     return  # Prevent saving duplicate record
        
        # Proceed with the normal save behavior
        super().save_model(request, obj, form, change)
        # Optionally suppress the success message here if needed
        self.message_user(request, "Water read saved successfully.", level=messages.SUCCESS)

    
    # Optionally, override save related method to prevent showing success
    def response_change(self, request, obj):
        # Customize the response message
        if obj.schedule and obj.schedule == 'OFF':
            # Prevent success message from showing
            return super().response_change(request, obj)
        return super().response_change(request, obj)

    # 2. Filter 'Read' records by 'Season' month and year
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        try:
            current_season = Season.objects.latest('MONTH_ID')  # Fetch the latest Season
        except Season.DoesNotExist:
            current_season = None

        if current_season:
            queryset = queryset.filter(month=current_season.MONTH_ENGLISH, year=current_season.YEAR)
        else:
            queryset = queryset.none()  # No season found, return no records
        
        return queryset


    class Meta:
        model = WaterRead

admin.site.register(WaterRead, WaterReadAdmin)

class ConsumptionZeroCountAdmin(admin.ModelAdmin):
    fields = ['code', 'year', 'consecutive_zero_count']
    list_display = ['id', 'code', 'year', 'consecutive_zero_count']
    search_fields = ['code']
    # list_filter = (('zone', RelatedOnlyFieldListFilter),)
    list_filter = ('consecutive_zero_count', 'year',)
    list_display_links = ['id', 'code', 'year', 'consecutive_zero_count']
    readonly_fields = ('id', 'code', 'year', 'consecutive_zero_count',)
    list_per_page = 10
    list_max_show_all = 500
    list_select_related = True
    
    def get_search_results(self, request, queryset, search_term):
        # Check if the search term includes a comparison operator
        if search_term:
            comparison_operator = None
            if '<=' in search_term:
                comparison_operator = '<='
            elif '>=' in search_term:
                comparison_operator = '>='
            elif '<' in search_term:
                comparison_operator = '<'
            elif '>' in search_term:
                comparison_operator = '>'
            elif '==' in search_term:
                comparison_operator = '=='

            # Extract the number from the search term
            if comparison_operator:
                try:
                    value = float(search_term.split(comparison_operator)[1].strip())
                except (ValueError, IndexError):
                    value = None
                
                if value is not None:
                    if comparison_operator == '<':
                        queryset = queryset.filter(consecutive_zero_count__lt=value)
                    elif comparison_operator == '<=':
                        queryset = queryset.filter(consecutive_zero_count__lte=value)
                    elif comparison_operator == '>':
                        queryset = queryset.filter(consecutive_zero_count__gt=value)
                    elif comparison_operator == '>=':
                        queryset = queryset.filter(consecutive_zero_count__gte=value)
                    elif comparison_operator == '==':
                        queryset = queryset.filter(consecutive_zero_count=value)

                search_term = ''  # Clear the search term to avoid default filtering
        
        return super().get_search_results(request, queryset, search_term)
    
    class Meta:
        model = ConsumptionZeroCount

admin.site.register(ConsumptionZeroCount, ConsumptionZeroCountAdmin)

class ReaderComparisonAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'name', 'month', 'year', 'rank_by_readings', 'status', 'zone', 'readings_count', 'total_consumption', 'discrepancies')
    list_display_links = ('id', 'name', 'month', 'year', 'status', 'zone', 'readings_count', 'total_consumption', 'discrepancies', 'rank_by_readings') 
    
    # Filters for easy navigation
    list_filter = ('status', 'zone',)
    
    # Enable search by grade and section
    search_fields = ('name', 'zone',)
    
    # Default ordering
    ordering = ('rank_by_readings',)
    
    # Add grouping and read-only fields for the view
    readonly_fields = ('id', 'name', 'status', 'zone', 'readings_count', 'total_consumption', 'discrepancies', 'rank_by_readings',)
    
    # Admin display customization
    fieldsets = (
        ("Reader Details", {
            "fields": ('id', 'name', 'status', 'zone'),
            "description": "Displays reader details.",
        }),
        ("Student Count", {
            "fields": ('readings_count', 'total_consumption', 'discrepancies', 'rank_by_readings',),
            "description": "Shows the total reading count, total consumption,  discrepancies and rank by readings of each reader combination.",
        }),
    )
    
    
    class Meta:
        model = ReaderComparison

admin.site.register(ReaderComparison, ReaderComparisonAdmin)

