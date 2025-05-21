from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
from .models import *
from django.db import connection, transaction
from django.contrib import messages
from django import forms
# Register your models here.

class SeasonAdmin(admin.ModelAdmin):
    # pass
    fields = ['MONTH_ID', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR_ID', 'YEAR']
    list_display = ['MONTH_ID', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR_ID', 'YEAR']
    search_fields = ['MONTH_ID']
    list_filter = ['MONTH_AMHARIC']
    list_display_links = ['MONTH_ID', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR_ID', 'YEAR']
    readonly_fields = ('MONTH_ID', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR_ID', 'YEAR',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = Season

admin.site.register(Season, SeasonAdmin)

class InputDataCurrentSeasonForm(forms.ModelForm):
    class Meta:
        model = InputDataCurrentSeason
        fields = ['month', 'year']
        # fields = ['uploaded_file']
        widgets = {
            'mid_id': forms.HiddenInput(),
            'yid_id': forms.HiddenInput(),
        }

# class InputDataCurrentSeasonAdmin(admin.ModelAdmin):
#     # fields = ['mid', 'month_id', 'yid', 'year_id']
#     actions = ['run_stored_procedure']

#     def run_stored_procedure(self, request, queryset):
#         for input_data in queryset:
#             with connection.cursor() as cursor:
#                 cursor.execute("CALL `season_change`(%s, %s, %s, %s)", [input_data.mid, input_data.month, input_data.yid, input_data.year])

#     run_stored_procedure.short_description = "Season Change"

# admin.site.register(InputDataCurrentSeason, InputDataCurrentSeasonAdmin)

class InputDataCurrentSeasonAdmin(admin.ModelAdmin):
    actions = ['run_stored_procedure']

    @transaction.atomic
    def run_stored_procedure(self, request, queryset):
        try:
            for input_data in queryset:
                mid = input_data.mid_id
                month = input_data.month_id
                yid = input_data.yid_id  # Adjust based on actual field name
                year = input_data.year_id  # Adjust based on actual field name

                # Log the values for debugging
                self.message_user(request, f"Calling stored procedure with mid={mid}, month={month}, yid={yid}, year={year}", messages.INFO)

                # Check for None values
                if None in [mid, month, yid, year]:
                    self.message_user(request, f"Skipping {input_data} due to missing data.", messages.WARNING)
                    continue

                with connection.cursor() as cursor:
                    cursor.callproc('season_change', [mid, month, yid, year])

            self.message_user(request, "Season changed successfully.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error: {str(e)}", messages.ERROR)

    run_stored_procedure.short_description = "Season change"

admin.site.register(InputDataCurrentSeason, InputDataCurrentSeasonAdmin)


