from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.utils.html import format_html

class CounterNumberInline(admin.TabularInline):  # or admin.StackedInline
    model = CounterNumber
    extra = 1  # Allows adding one extra inline form

@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    inlines = [CounterNumberInline]
    list_display = ['id', 'amharic_full_name', 'customer_image_preview', 'english_full_name', 'code', 'gender', 'marital_status']
    list_display_links = ['id', 'amharic_full_name', 'customer_image_preview', 'gender', 'marital_status']
    search_fields = ['id', 'amharic_full_name', 'english_full_name', 'code', 'email', 'contact_number']
    list_filter = ['kebele__kebele', 'zone__zone', 'service_type__service', 'month', 'year']
    list_per_page = 18
    list_editable = ['english_full_name']
    list_select_related = True
    readonly_fields = ('id', 'created_by', 'created_at', 'modified_by', 'modified_at', 'customer_image_preview_on_form')
    
    fieldsets = (
        ('Name Information', {
            'fields': (('amharic_full_name', 'english_full_name'),)
        }),
        ('Personal Details', {
            'fields': (('gender', 'marital_status'),)
        }),
        ('Contact Information', {
            'fields': (('contact_number', 'email'),)
        }),
        ('Address Information', {
            'fields': (('destrict', 'kebele'), ('place_name', 'zone'), 'house_number')
        }),
        ('Service Information', {
            'fields': (('code', 'service_type'), ('guage_width', 'deposit'))
        }),
        ('Reading Schedule', {
            'fields': (('month', 'year'), ('initial_read', 'first_read'), 'read_date')
        }),
        ('Contract & Status', {
            'fields': (('contract_number', 'customer_status'),)
        }),
        ('Documents', {
            'fields': (('customer_image', 'contract_file'), 'customer_image_preview_on_form')
        }),
        ('System Info (Read-only)', {
            'fields': (('id', 'created_by', 'created_at'), ('modified_by', 'modified_at'))
        }),
    )
    
    def get_search_results(self, request, queryset, search_term):
        # call the original method to get initial results
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # override the search to use exact match for the 'name' field
            queryset = self.model.objects.filter(code__exact=search_term)

        return queryset, use_distinct
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'customer_image':
            formfield.widget.attrs['style'] = 'max-width: 300px;'
            formfield.widget.attrs['class'] = 'vImageField'
        return formfield

    def customer_image_preview(self, obj):
        if obj.customer_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height: 50px; border-radius: 5px;"/></a>',
                obj.customer_image.url,
                obj.customer_image.url
            )
        return "No Image"
    customer_image_preview.short_description = "Customer Image"

    def customer_image_preview_on_form(self, obj):
        if obj.customer_image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 300px; border-radius: 10px; border: 1px solid #ccc;"/>',
                obj.customer_image.url
            )
        return "No Image"
    customer_image_preview_on_form.short_description = "Image Preview"

class RenewContractAdmin(ImportExportModelAdmin):
    pass
    fields = [('id'), ('full_name', 'gender'), ('contact_number', 'code'), ('kebele', 'place_name'), ('zone', 'house_number'), ('service_type', 'guage_width'), ('month', 'year'), ('customer_status', 'created_at'), ('number_of_years')]
    list_display = ['id', 'full_name', 'gender', 'contact_number', 'code', 'kebele', 'place_name', 'zone', 'house_number']
    search_fields = ['id', 'full_name', 'contact_number', 'code']
    list_filter = ['kebele', 'zone', 'service_type', 'month', 'year']
    list_display_links = ['id', 'full_name', 'gender', 'contact_number', 'code', 'kebele', 'place_name', 'zone', 'house_number']
    readonly_fields = ('id', 'full_name', 'gender', 'contact_number', 'code', 'kebele', 'place_name', 'zone', 'house_number', 'service_type', 'guage_width', 'month', 'year', 'customer_status', 'created_at', 'number_of_years',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = RenewContract

admin.site.register(RenewContract, RenewContractAdmin)

class ConsiderationFreeAdmin(ImportExportModelAdmin):
    pass
    fields = [('id'), ('full_name', 'gender'), ('contact_number', 'code'), ('kebele', 'place_name'), ('zone', 'house_number'), ('service_type', 'guage_width'), ('month', 'year'), ('customer_status', 'created_at'), ('number_of_years')]
    list_display = ['id', 'full_name', 'gender', 'number_of_years', 'contact_number', 'code', 'kebele', 'place_name', 'zone', 'house_number']
    search_fields = ['id', 'full_name', 'contact_number', 'code']
    list_filter = ['kebele', 'zone', 'service_type', 'month', 'year']
    list_display_links = ['id', 'full_name', 'gender', 'number_of_years', 'contact_number', 'code', 'kebele', 'place_name', 'zone', 'house_number']
    readonly_fields = ('id', 'full_name', 'gender', 'contact_number', 'code', 'kebele', 'place_name', 'zone', 'house_number', 'service_type', 'guage_width', 'month', 'year', 'customer_status', 'created_at', 'number_of_years',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = ConsiderationFree

admin.site.register(ConsiderationFree, ConsiderationFreeAdmin)

class ClearanceAdmin(ImportExportModelAdmin):
    pass
    fields = [('id'), ('full_name', 'gender'), ('contact_number', 'code'), ('deposit', 'total_bill'), ('balance')]
    list_display = ['id', 'code', 'full_name', 'gender', 'contact_number', 'deposit', 'total_bill', 'balance']
    search_fields = ['id', 'full_name', 'contact_number', 'code']
    list_filter = ['gender']
    list_display_links = ['id', 'code', 'full_name', 'gender', 'contact_number', 'deposit', 'total_bill', 'balance']
    readonly_fields = ('id', 'code', 'full_name', 'gender', 'contact_number', 'deposit', 'total_bill', 'balance',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = Clearance

admin.site.register(Clearance, ClearanceAdmin)

# class ClientAdmin(ImportExportModelAdmin):
# 	"""docstring for ClientAdmin"""
# 	# pass
# 	list_display = ['Client_id', 'Amharic_first_name', 'Amharic_father_name', 'Amharic_last_name']
# 	search_fields = ['Client_id']
# 	list_filter = ['Read_date_at']
# 	list_display_links = ['Client_id', 'Amharic_first_name', 'Amharic_father_name', 'Amharic_last_name']

# 	class Meta:
# 		model = Client

# admin.site.register(Client, ClientAdmin)

# admin.site.register(WaterRead)
# admin.site.register(WaterBill)