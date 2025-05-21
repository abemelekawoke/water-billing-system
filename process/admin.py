# from django.db import models
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection

from django.http import HttpResponse
# import csv
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.utils.html import format_html
from import_export.admin import ExportMixin
from import_export import resources

# from django.contrib.auth.models import Group

class GeneralLeisureAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Tasks','Dates'),('Year', 'Month'), ('General','Check_no','Check_payable','Receipt_no')],
        }), 
		('Detail information', {
			'fields': [('Deposit','Withdraw','Balance')],
		}),
    ]
    list_display = ['id','Dates','Tasks','Deposit','Withdraw','Balance','General','Check_no','Receipt_no']
    search_fields = ['id','Dates','Tasks','Deposit','Withdraw','Balance','General','Check_no','Receipt_no']
    list_filter = ['Dates', 'Year', 'Month']
    list_display_links = ['id','Dates','Tasks','Deposit','Withdraw','Balance','General','Check_no','Receipt_no']
    readonly_fields = ('id','Balance','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = GeneralLeisure	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(GeneralLeisure, GeneralLeisureAdmin)

class RevenueTypeAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('Detail informations', {
            'fields': ['Dates', ('department', 'Revenue_title_amharic'), ('Code', 'Revenue_annual_plan'), ('Measurement', 'Year')],
        }), 
    ]
    list_display = ['id','Dates','department','Code','Measurement', 'Year', 'Revenue_title_amharic','Revenue_annual_plan']
    search_fields = ['id','Dates','department__name','Code','Revenue_title_amharic__name', 'Year']
    list_filter = ['department__name', 'Code', 'Year']
    list_display_links = ['id','Dates','department','Code','Measurement', 'Year', 'Revenue_title_amharic','Revenue_annual_plan']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = RevenueType	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(RevenueType, RevenueTypeAdmin)

class RevenueAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('Detail informations', {
            'fields': [('Dates', 'Code'), 'Amount', ('Year', 'Month')],
        }), 
    ]
    list_display = ['id','Dates','Year', 'Month','Code','Amount']
    search_fields = ['id','Dates','Code','Amount', 'Year']
    list_filter = ['Dates']
    list_display_links = ['id','Dates','Year', 'Month','Code','Amount']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = AllRevenue	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(AllRevenue, RevenueAdmin)

class ExpenseTypeAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('Detail informations', {
            'fields': ['Dates', ('department', 'Expense_title_amharic'), ('Code', 'Expense_annual_plan'), ('Measurement', 'Year')],
        }), 
    ]
    list_display = ['id','Dates','department','Code','Measurement', 'Year', 'Expense_title_amharic', 'Expense_annual_plan']
    search_fields = ['id','Dates','department','Code','Year', 'Expense_title_amharic','']
    list_filter = ['department__name', 'Code', 'Year']
    list_display_links = ['id','Dates','department','Measurement', 'Year','Code','Expense_title_amharic', 'Expense_annual_plan']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = ExpenseType	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(ExpenseType, ExpenseTypeAdmin)

class ExpenseAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('Detail informations', {
            'fields': [('Dates', 'Code'), 'Amount', ('Year', 'Month')],
        }), 
    ]
    list_display = ['id','Dates','Year', 'Month','Code','Amount']
    search_fields = ['id','Dates','Code','Amount']
    list_filter = ['Dates']
    list_display_links = ['id','Dates','Year', 'Month','Code','Amount']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = AllExpense	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(AllExpense, ExpenseAdmin)

# Potable water service starts here
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PotableWaterServiceType

class PotableWaterServiceTypeAdmin(ImportExportModelAdmin):
    fieldsets = [
        ('Detail information', {
            'fields': ['Dates', ('department', 'Service_title_amharic'), ('Service_annual_plan'), ('Measurement', 'Year')],
        }), 
    ]
    
    list_display = ['id', 'Dates', 'department', 'Measurement', 'Year', 'Service_title_amharic', 'Service_annual_plan']
    search_fields = ['id', 'Dates', 'department', 'Service_title_amharic']
    list_filter = ['department__name', 'Service_title_amharic', 'Year']
    list_display_links = ['id', 'Dates', 'department', 'Measurement', 'Year', 'Service_title_amharic', 'Service_annual_plan']
    readonly_fields = ('id', 'Registered_date', 'Updated_by', 'Registered_by')
    list_per_page = 10
    list_select_related = True

    class Meta:
        model = PotableWaterServiceType

    def save_model(self, request, obj, form, change):
        if change:
            obj.Updated_by = request.user
            obj.Registered_date = datetime.now()
        obj.save()

admin.site.register(PotableWaterServiceType, PotableWaterServiceTypeAdmin)

class AllPotableWaterServiceManagementAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('Detail informations', {
            'fields': [('Dates','Code'), 'Amount', ('Year', 'Month')],
        }), 
    ]
    list_display = ['id','Dates','Year', 'Month','Code','Amount']
    search_fields = ['id','Dates','Code','Amount', 'Year']
    list_filter = ['Dates']
    list_display_links = ['id','Dates','Year', 'Month','Code','Amount']
    readonly_fields = ('id','Registered_date','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = AllPotableWaterServiceManagement	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Registered_date = datetime.now()
	    obj.save()

admin.site.register(AllPotableWaterServiceManagement, AllPotableWaterServiceManagementAdmin)

# class ServiceTypeInlineAdmin(admin.TabularInline):
# 	model = ServiceTypeInline
# 	extra = 0
# 	list_filter = ['Service_type']
# 	# readonly_fields = ['Quantity']

class MaterialAdminInline(admin.TabularInline):
	model = MaterialInline
	extra = 0
	list_filter = ['Name']
	readonly_fields = ['Single_price', 'Total_price']

class DetailCostManagementAdmin(ImportExportModelAdmin):
    inlines = [MaterialAdminInline] 
    fieldsets = [
        ('General informations', {
            'fields': [('Full_name', 'Kebele'), ('House_number', 'Customer_neighbor'), ('Customer_type'), ('Address', 'Phone_number'), ('Place', 'Line_joined'), ('Year', 'Month'), ('Officer','Process_status')],
        }),
        ('Approval Requests', {
            'fields': ['Potable_water', 'Income_office', 'Amount', 'Cashier'],
        }),
        ('Materials information', {
            'fields': [('Material_cost', 'Total_60', 'Total_25'), 'Grand_total'],
        }),
        ('Detail information', {
            'fields': [('Deposite', 'For_Digging', 'For_Rope', 'For_Agreement', 'For_Forms', 'For_consultation', 'For_information')],
        }),
    ]
    list_display = ['id', 'Full_name', 'Kebele', 'House_number', 'Customer_type', 'Customer_neighbor', 'Total_60', 'Total_25', 'Deposite', 'For_Digging', 'For_Rope', 'For_Agreement', 'For_Forms', 'Total_Form', 'Grand_total', 'Potable_water', 'Income_office', 'Amount', 'Cashier', 'Requested_at', 'Updated_by', 'Registered_by']
    search_fields = ['id', 'Full_name', 'Kebele', 'House_number', 'Phone_number', 'Customer_neighbor']
    list_filter = ['Customer_type']
    list_display_links = ['id', 'Full_name', 'Kebele', 'House_number', 'Customer_type', 'Customer_neighbor', 'Total_60', 'Total_25', 'Deposite', 'For_Digging', 'For_Rope', 'For_Agreement', 'For_Forms', 'Total_Form', 'Grand_total', 'Potable_water', 'Income_office', 'Amount', 'Cashier', 'Requested_at', 'Updated_by', 'Registered_by']
    readonly_fields = ('id', 'Grand_total', 'Requested_at', 'Updated_by', 'Registered_by')
    list_per_page = 10
    list_select_related = True

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(DetailCostManagementAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(DetailCostManagementAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        if obj.pk:
            invoice_lines = MaterialInline.objects.filter(Detail_cost_management=obj.id)
            obj.Material_cost = 0
            for line in invoice_lines:
                obj.Material_cost += line.Total_price
            obj.Total_25 = (obj.Material_cost * 25) / 100
            obj.Total_60 = (obj.Material_cost * 60) / 100
            obj.Grand_total = Decimal(obj.Material_cost) + Decimal(obj.Total_25) + Decimal(obj.Total_60) + obj.Deposite + obj.For_Digging + obj.For_Rope + obj.For_Agreement + obj.For_Forms + obj.For_consultation + obj.For_information

            obj.save()  # Save the updated object
        return obj

    class Meta:
	    model = DetailCostManagement	
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.Updated_by = request.user
            obj.Requested_at = datetime.now()
        obj.save()

admin.site.register(DetailCostManagement, DetailCostManagementAdmin)

# Define resource for export
class DepartmentPerformanceRankResource(resources.ModelResource):
    class Meta:
        model = DepartmentPerformanceRank
        fields = ("id", "department", "month", "year", "total_plan", "total_performed", "performance_percentage", "rank")
        export_order = ("id", "department", "month", "year", "total_plan", "total_performed", "performance_percentage", "rank")

@admin.register(DepartmentPerformanceRank)
class DepartmentPerformanceRankAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DepartmentPerformanceRankResource  # Enables export options
    list_display = ["id", "department", "rank_display", "month", "year", "total_plan", "total_performed", "formatted_percentage"]
    list_display_links = ["id", "department", "rank_display", "month", "year", "total_plan", "total_performed", "formatted_percentage"]
    list_filter = ["department", "month", "year"]
    search_fields = ["department__name"]
    ordering = ["rank", "-performance_percentage"]  # Show best performing first
    readonly_fields = ("id", "rank", "performance_percentage")  # Prevent editing computed fields
    list_per_page = 15  
    list_select_related = True  # Optimizes database queries

    fieldsets = (
        ("Department Information", {
            "fields": ("department", "month", "year"),
            "classes": ("wide",),  
        }),
        ("Performance Data", {
            "fields": ("total_plan", "total_performed", "performance_percentage", "rank"),
            "classes": ("collapse",),  
        }),
    )

    def formatted_percentage(self, obj):
        """Displays percentage with % sign and two decimal places"""
        return f"{obj.performance_percentage:.2f}%"
    
    formatted_percentage.short_description = "Performance %"
    
    def rank_display(self, obj):
        """Color-coded ranking"""
        if obj.rank == 1:
            color = "gold"
        elif obj.rank <= 3:
            color = "green"
        elif obj.rank <= 5:
            color = "orange"
        else:
            color = "red"
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.rank}</span>')
    
    rank_display.short_description = "Rank"
    rank_display.admin_order_field = "rank"
