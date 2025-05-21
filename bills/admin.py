from django.contrib import admin
from .models import *
import requests
from django import forms
from django.db import connection, transaction
from django.contrib import messages
from import_export.admin import ImportExportModelAdmin
# start
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import tempfile
import os
from escpos.printer import Usb

from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.utils.html import format_html

from django.urls import reverse
# end
from django.utils.dateparse import parse_date
from django.utils.safestring import mark_safe
from django.db.models import Sum
from django.contrib import admin
from .models import WaterBill
from datetime import datetime

from django.db.models import Q
from django.utils.html import format_html

class WaterBillAdmin(ImportExportModelAdmin):
    fields = [('id', 'code'), ('month', 'year'), ('previous_read', 'current_read'),
              ('consumption', 'guage_rent'), ('block1', 'block2'), ('block3', 'block4'),
              ('block5', 'bill_id'), ('current_price', 'total_price'), ('payment_start', 'payment_end'),
              ('status'), ('created_by', 'created_at'), ('modified_by', 'modified_at')]

    list_display = ['id', 'code', 'consumption', 'bill_id', 'guage_rent', 'current_price', 'total_price',
                    'status', 'formatted_payment_start', 'formatted_payment_end',
                    'payment_start', 'payment_end', 'month', 'year', 'previous_read', 'current_read',
                    'created_by', 'created_at', 'modified_by', 'modified_at']

    search_fields = ['code', 'bill_id']
    list_editable = ['status', 'payment_start', 'payment_end']
    list_filter = ['month', 'year']
    list_display_links = ['id', 'code', 'consumption', 'bill_id', 'guage_rent', 'current_price', 'total_price', 'month', 'year']
    readonly_fields = ('id', 'created_by', 'created_at', 'modified_by', 'modified_at',)
    list_per_page = 27
    def get_search_results(self, request, queryset, search_term):
        # call the original method to get initial results
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # override the search to use exact match for the 'name' field
            queryset = self.model.objects.filter(code__exact=search_term)

        return queryset, use_distinct
    # list_select_related = False
    
    # def get_search_results(self, request, queryset, search_term):
    #     queries = Q()
    #     for field in self.search_fields:
    #         queries |= Q(**{f"{field}__exact": search_term})
    #     queryset = queryset.filter(queries)
    #     return queryset, False

    @admin.display(description='Payment Start')
    def formatted_payment_start(self, obj):
        return obj.payment_start.strftime('%m/%d/%Y') if obj.payment_start else ''

    @admin.display(description='Payment End')
    def formatted_payment_end(self, obj):
        return obj.payment_end.strftime('%m/%d/%Y') if obj.payment_end else ''

    from datetime import datetime, date

    def save_model(self, request, obj, form, change):
        # Ensure payment_start and payment_end are in the correct format only if they're strings
        if obj.payment_start and isinstance(obj.payment_start, str):
            try:
                obj.payment_start = datetime.strptime(obj.payment_start, '%m/%d/%Y').date()
            except ValueError:
                raise ValueError("Incorrect date format for payment_start. Expected MM/DD/YYYY.")

        if obj.payment_end and isinstance(obj.payment_end, str):
            try:
                obj.payment_end = datetime.strptime(obj.payment_end, '%m/%d/%Y').date()
            except ValueError:
                raise ValueError("Incorrect date format for payment_end. Expected MM/DD/YYYY.")
        
        # Save the model
        super().save_model(request, obj, form, change)


    def print_receipt(self, request, queryset):
        for bill in queryset:
            try:
                pdf_path = self.generate_pdf(bill)  # Generate PDF
                self.send_to_printer(pdf_path)      # Send PDF to printer
                os.remove(pdf_path)                 # Clean up temporary file
                self.message_user(request, f"Receipt for bill {bill.code} printed successfully!", level=messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Failed to print receipt for bill {bill.code}: {str(e)}", level=messages.ERROR)

    print_receipt.short_description = "Print Water Bill Receipt"

    def generate_pdf(self, bill):
        # Generate PDF receipt and return the file path
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf = canvas.Canvas(temp_file.name)
        
        pdf.setFont("Helvetica", 14)
        pdf.drawString(100, 750, "Water Bill Receipt")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 730, f"Code: {bill.code}")
        pdf.drawString(100, 710, f"Month: {bill.month} - {bill.year}")
        pdf.drawString(100, 690, f"Previous Read: {bill.previous_read}")
        pdf.drawString(100, 670, f"Current Read: {bill.current_read}")
        pdf.drawString(100, 650, f"Consumption: {bill.consumption} m³")
        pdf.drawString(100, 630, f"Total Price: ${bill.total_price}")
        pdf.drawString(100, 610, f"Payment End Date: {bill.payment_end}")
        pdf.drawString(100, 590, "----------------------")
        pdf.drawString(100, 570, "Thank you for your payment!")
        
        pdf.save()
        return temp_file.name

    def send_to_printer(self, pdf_path):
        try:
            # Adjust vendor_id and product_id for your USB printer
            printer = Usb(0x0FE6, 0x811E)  # Update with your printer's IDs
            
            # For printing text, you would use something like:
            # printer.text("Your receipt data here")
            
            # For printing PDF directly, we can convert PDF to an image (not ideal for direct print)
            # A better approach would be converting PDF to an image and then printing the image.
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            
            printer._raw(pdf_data)  # Send raw PDF data to printer (works only if supported)
            printer.cut()  # Cut the paper
            
        except Exception as e:
            raise Exception(f"Printing failed: {str(e)}")

    actions = [print_receipt]  # Add the action to the admin panel

    class Meta:
        model = WaterBill

admin.site.register(WaterBill, WaterBillAdmin)

class InputDataAdmin(admin.ModelAdmin):
    actions = ['run_stored_procedure']

    @transaction.atomic
    def run_stored_procedure(self, request, queryset):
        try:
            user_id = request.user.id  # Get logged-in user's ID
            
            for input_data in queryset:
                kebele = input_data.kebele
                zone = input_data.zone
                month = input_data.month  # Adjust based on actual field name
                year = input_data.year  # Adjust based on actual field name

                # Log the values for debugging
                self.message_user(request, f"Calling stored procedure with kebele={kebele}, zone={zone}, month={month}, year={year}, user_id={user_id}", messages.INFO)

                # Check for None values
                if None in [kebele, zone, month, year, user_id]:
                    self.message_user(request, f"Skipping {input_data} due to missing data.", messages.WARNING)
                    continue

                with connection.cursor() as cursor:
                    cursor.callproc('InsertWaterBillAndRead', [kebele, zone, month, year, user_id, user_id])

            self.message_user(request, "Bills calculated successfully.", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error: {str(e)}", messages.ERROR)

    run_stored_procedure.short_description = "Calculate bills"

admin.site.register(InputData, InputDataAdmin)


class UnsoldBillsAdmin(ImportExportModelAdmin):
    # pass
    fields = [('id'), ('code', 'unsold_price'), ('unsold_months', 'penalty'), ('total_penalty', 'total_price')]
    list_display = ['id', 'code', 'unsold_price', 'unsold_months', 'penalty', 'total_penalty', 'total_price']
    search_fields = ['id', 'code']
    list_filter = ['unsold_months']
    list_display_links = ['id', 'code', 'unsold_price', 'unsold_months', 'penalty', 'total_penalty', 'total_price']
    readonly_fields = ('id',)
    list_per_page = 27
    list_select_related = True
    
    def has_change_permission(self, request, obj=None):
        # Show a message to the user
        # messages.error(request, "This view is read-only and cannot be edited.")
        return False  # Prevent change permission
    
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
                        queryset = queryset.filter(unsold_months__lt=value)
                    elif comparison_operator == '<=':
                        queryset = queryset.filter(unsold_months__lte=value)
                    elif comparison_operator == '>':
                        queryset = queryset.filter(unsold_months__gt=value)
                    elif comparison_operator == '>=':
                        queryset = queryset.filter(unsold_months__gte=value)
                    elif comparison_operator == '==':
                        queryset = queryset.filter(unsold_months=value)

                search_term = ''  # Clear the search term to avoid default filtering
        
        return super().get_search_results(request, queryset, search_term)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = UnsoldBills

admin.site.register(UnsoldBills, UnsoldBillsAdmin)

class HandoverDetailReportAdmin(ImportExportModelAdmin):
    fieldsets = [
        ('General information', {
            'fields': ['CODE', 'KEBELE', 'ZONE', 'SERVICE'],
        }),
        ('Date information', {
            'fields': ['CONSUMPTION', 'TOTAL_PRICE', 'MONTH', 'YEAR'],
        }),
    ]
    list_display = ['ID', 'CODE', 'KEBELE', 'ZONE', 'SERVICE', 'CONSUMPTION', 'TOTAL_PRICE', 'MONTH', 'YEAR']
    search_fields = ['ID', 'CODE', 'KEBELE', 'ZONE', 'SERVICE', 'CONSUMPTION', 'TOTAL_PRICE', 'MONTH', 'YEAR']
    list_filter = ['MONTH', 'YEAR']
    list_display_links = ['ID', 'CODE', 'KEBELE', 'ZONE', 'SERVICE', 'CONSUMPTION', 'TOTAL_PRICE', 'MONTH', 'YEAR']
    readonly_fields = ('ID', 'CODE', 'KEBELE', 'ZONE', 'SERVICE', 'CONSUMPTION', 'TOTAL_PRICE', 'MONTH', 'YEAR')
    list_per_page = 10
    list_select_related = True
    # actions = [download_pdf]

    # def save_model(self, request, obj, form, change):
    #     if change:
    #         obj.Updated_by = request.user
    #     obj.Registered_at = timezone.now()
    #     obj.save()

admin.site.register(HandoverDetailReport, HandoverDetailReportAdmin)

@admin.register(HandoverSummaryReport)
class HandoverSummaryReportAdmin(ImportExportModelAdmin):
    list_display = (
        'kebele',
        'service_type',
        'customer_total',
        'total_consumption',
        'total_bills',
        'total_rent',
        'total_price',
        'month',
        'year',
    )
    search_fields = ('kebele', 'service_type', 'month', 'year')
    list_filter = ('month', 'year', 'service_type')
    ordering = ('kebele', '-year', '-month')
    readonly_fields = (
        'kebele',
        'customer_total',
        'service_type',
        'total_consumption',
        'total_bills',
        'total_rent',
        'total_price',
        'month',
        'year',
    )

    def has_add_permission(self, request):
        return False  # Prevent adding new entries

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of entries

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing

class PaidOnDateRangeFilter(admin.SimpleListFilter):
    title = _('Paid On Date')
    parameter_name = 'paid_on'

    def lookups(self, request, model_admin):
        return [
            ('today', _('Today')),
            ('past_7_days', _('Past 7 Days')),
            ('this_month', _('This Month')),
        ]

    def queryset(self, request, queryset):
        today = now().date()  # Get today's date
        value = self.value()

        if value == 'today':
            return queryset.annotate(date_only=TruncDate('paid_on')).filter(date_only=today)
        elif value == 'past_7_days':
            return queryset.annotate(date_only=TruncDate('paid_on')).filter(date_only__gte=today - timedelta(days=7))
        elif value == 'this_month':
            return queryset.annotate(date_only=TruncDate('paid_on')).filter(date_only__year=today.year, date_only__month=today.month)
        return queryset
    
class PaymentMethodAdmin(ImportExportModelAdmin):
    list_display = ("code", "kebele", "zone", "service", "month", "year", "bill_id", "rent", "current_price", "total_price", "paid_on", "colored_payment_method", "bank_name", "bank_transaction_reference")
    list_display_links = ("bill_id", "month", "year", "code", "kebele", "zone", "service", "rent", "current_price", "total_price", "paid_on", "colored_payment_method", "bank_name")
    list_filter = (PaidOnDateRangeFilter, "month", "year", "zone", "service", "payment_method", "bank_name")
    search_fields = ("bill_id", "code", "kebele", "zone", "service", "bank_transaction_reference", )
    ordering = ("-paid_on",)
    readonly_fields = ("bill_id", "code", "kebele", "zone", "service", "consumption", "total_price", "paid_on", "bank_transaction_reference", "bank_name", "month", "year", "payment_method")
    
    # def get_search_results(self, request, queryset, search_term):
    #     queries = Q()
    #     for field in self.search_fields:
    #         queries |= Q(**{f"{field}__exact": search_term})
    #     queryset = queryset.filter(queries)
    #     return queryset, False
    # def get_search_results(self, request, queryset, search_term):
    #     # call the original method to get initial results
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)

    #     if search_term:
    #         # override the search to use exact match for the 'name' field
    #         queryset = self.model.objects.filter(code__exact=search_term)

    #     return queryset, use_distinct
    
    def colored_payment_method(self, obj):
        """Display payment method with color-coded labels"""
        color_map = {
            "Paid by Bank": "green",
            "Paid by Office": "blue",
            "Not Sold": "red"
        }
        color = color_map.get(obj.payment_method, "gray")
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.payment_method}</span>')

    colored_payment_method.admin_order_field = "payment_method"
    colored_payment_method.short_description = "Payment Status"

    fieldsets = (
        ("Payment Details", {
            "fields": ("code", "kebele", "zone", "service", "consumption", "bill_id", "rent", "current_price", "total_price", "month", "year")
        }),
        ("Bank Details", {
            "fields": ("paid_on", "bank_transaction_reference", "bank_name"),
        }),
        ("Status", {
            "fields": ("payment_method",),
        }),
    )

    list_per_page = 20  # Paginate for better UI

    def has_add_permission(self, request):
        return False  # Prevent adding new records

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing records

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of records

admin.site.register(PaymentMethod, PaymentMethodAdmin)

# class BankBalanceAdmin(admin.ModelAdmin):
#     list_display = ("bank_name", "formatted_total_balance", "transaction_count")
#     list_filter = ("bank_name",)
#     search_fields = ("bank_name",)
#     ordering = ("-total_balance",)  # Sorts by highest balance first
#     readonly_fields = ("id", "bank_name", "total_balance", "transaction_count")  # Read-only since it's unmanaged

#     def formatted_total_balance(self, obj):
#         return format_html('<b style="color: green;">${:,.2f}</b>', obj.total_balance)
    
#     formatted_total_balance.short_description = "Total Balance"

#     def has_add_permission(self, request):
#         return False  # Prevents adding new records

#     def has_change_permission(self, request, obj=None):
#         return False  # Prevents modifying records

#     def has_delete_permission(self, request, obj=None):
#         return False  # Prevents deleting records
    
# admin.site.register(BankBalance, BankBalanceAdmin)

@admin.register(BankBalance)
class BankBalanceAdmin(ImportExportModelAdmin):
    list_display = ('colored_id', 'bank_link', 'formatted_balance', 
                   'transaction_count', 'average_transaction', 'balance_indicator')
    list_display_links = None
    list_filter = ('bank_name',)
    search_fields = ('bank_name',)
    ordering = ('-total_balance',)
    readonly_fields = ('bank_details',)
    
    fieldsets = (
        (None, {
            'fields': ('bank_details',),
        }),
    )

    def colored_id(self, obj):
        return format_html(
            '<span style="display:inline-block;width:40px;color:#666;font-weight:bold;">#{}</span>',
            obj.id
        )
    colored_id.short_description = 'ID'

    def bank_link(self, obj):
        url = reverse('admin:bills_bankbalance_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="font-weight:600;color:#267f99;text-decoration:none;">{}</a>',
            url,
            obj.bank_name
        )
    bank_link.short_description = 'Bank Name'

    def formatted_balance(self, obj):
        color = '#2e7d32' if obj.total_balance >= 10000 else '#d32f2f'
        icon = '↑' if obj.total_balance >= 10000 else '↓'
        amount = "${:,.2f}".format(obj.total_balance)
        return format_html(
            '<div style="font-family:monospace;font-weight:600;color:{};white-space:nowrap;">'
            '<span style="font-size:0.8em;margin-right:3px;">{}</span>{}</div>',
            color, icon, amount
        )
    formatted_balance.short_description = 'Total Balance'

    def average_transaction(self, obj):
        if obj.transaction_count > 0:
            avg = obj.total_balance / obj.transaction_count
            color = '#2e7d32' if avg >= 500 else '#d32f2f'
            amount = "${:,.2f}".format(avg)
            return format_html(
                '<div style="font-family:monospace;color:{};white-space:nowrap;">{}</div>',
                color, amount
            )
        return format_html('<div style="color:#666;">$0.00</div>')
    average_transaction.short_description = 'Avg. Transaction'
    
    def balance_indicator(self, obj):
        total = BankBalance.objects.aggregate(Sum('total_balance'))['total_balance__sum'] or 1
        percentage = (obj.total_balance / total) * 100
        percentage_text = "{:.1f}%".format(percentage)
        percentage_value = min(percentage, 100)
        
        return format_html(
            '<div title="{} market share" style="background:#e0e0e0;height:20px;border-radius:10px;width:100%;position:relative;margin-top:5px;">'
            '<div style="background:#4caf50;height:100%;border-radius:10px;width:{}%;"></div>'
            '<div style="position:absolute;top:0;left:0;width:100%;text-align:center;line-height:20px;font-size:11px;color:#333;">{}</div>'
            '</div>',
            percentage_text,
            percentage_value,
            percentage_text
        )
    balance_indicator.short_description = 'Market Share'

    def bank_details(self, obj):
        total = BankBalance.objects.aggregate(Sum('total_balance'))['total_balance__sum'] or 1
        percentage = (obj.total_balance / total) * 100
        percentage_text = "{:.1f}%".format(percentage)
        percentage_value = min(percentage, 100)
        
        return format_html(
            '<div style="margin-bottom:20px;font-family:Arial,sans-serif;">'
            '<h2 style="color:#ffffff;background-color:#267f99;border-bottom:1px solid #1a5c73;padding:10px 15px;margin-top:0;border-radius:4px 4px 0 0;">{} Bank Summary</h2>'
            
            '<div style="display:flex;flex-wrap:wrap;gap:20px;margin-top:20px;">'
            '<div style="flex:1;min-width:250px;background:#f8f9fa;padding:15px;border-radius:5px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">'
            '<h3 style="margin-top:0;color:#555;font-size:16px;">Balance Information</h3>'
            '<table style="width:100%;border-collapse:collapse;">'
            '<tr><td style="padding:8px 0;border-bottom:1px solid #eee;font-weight:600;color:#555;">Total Balance:</td>'
            '<td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;font-family:monospace;">{}</td></tr>'
            '<tr><td style="padding:8px 0;border-bottom:1px solid #eee;font-weight:600;color:#555;">Transactions:</td>'
            '<td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">{}</td></tr>'
            '<tr><td style="padding:8px 0;font-weight:600;color:#555;">Avg. Transaction:</td>'
            '<td style="padding:8px 0;text-align:right;font-family:monospace;">{}</td></tr>'
            '</table>'
            '</div>'
            
            '<div style="flex:1;min-width:250px;background:#f8f9fa;padding:15px;border-radius:5px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">'
            '<h3 style="margin-top:0;color:#555;font-size:16px;">Market Share</h3>'
            '<div style="text-align:center;margin:15px 0;font-size:24px;font-weight:bold;color:#4caf50;">{}</div>'
            '<div style="background:#e0e0e0;height:20px;border-radius:10px;width:100%;margin-top:10px;">'
            '<div style="background:#4caf50;height:100%;border-radius:10px;width:{}%;"></div>'
            '</div>'
            '</div>'
            '</div>',
            obj.bank_name,
            self.formatted_balance(obj),
            obj.transaction_count,
            self.average_transaction(obj),
            percentage_text,
            percentage_value
        )
    bank_details.short_description = ''

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['css'] = """
            <style>
                #result_list td, #result_list th {
                    padding: 12px 8px;
                    vertical-align: middle;
                }
                #result_list tr:hover td {
                    background-color: #f8f9fa;
                }
                .balance-indicator {
                    min-width: 100px;
                }
            </style>
        """
        return super().changelist_view(request, extra_context=extra_context)
    
@admin.register(PaymentSummaryPeriod)
class PaymentSummaryPeriodAdmin(ImportExportModelAdmin):
    list_display = (
        'colored_service_type',
        'month',
        'year',
        'transaction_count',
        'bill_price',
        'guage_rent',
        'formatted_total_balance',
    )
    list_display_links = (
        'colored_service_type',
        'month',
        'year',
        'transaction_count',
        'bill_price',
        'guage_rent',
        'formatted_total_balance',
    )
    list_filter = (
        'service_type',
        'month',
        'year',
    )
    search_fields = (
        'service_type',
        'month',
        'year',
    )
    ordering = ('-year', '-month', '-total_balance')
    readonly_fields = [field.name for field in PaymentSummaryPeriod._meta.fields]
    list_per_page = 25

    def colored_service_type(self, obj):
        return format_html('<span style="color:#2c3e50;font-weight:500;">{}</span>', obj.service_type)
    colored_service_type.short_description = 'Service Type'

    def formatted_total_balance(self, obj):
        return f"{obj.total_balance:,.2f} ETB"
    formatted_total_balance.short_description = 'Total Balance'

    def has_add_permission(self, request):
        return False  # Prevent adding from admin

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion
    
@admin.register(UnsoldPaymentSummaryPeriod)
class UnsoldPaymentSummaryPeriodAdmin(ImportExportModelAdmin):
    list_display = (
        'colored_service_type',
        'month',
        'year',
        'customer_count',
        'bill_price',
        'guage_rent',
        'formatted_total_balance',
    )
    list_display_links = (
        'colored_service_type',
        'month',
        'year',
        'customer_count',
        'bill_price',
        'guage_rent',
        'formatted_total_balance',
    )
    list_filter = (
        'service_type',
        'month',
        'year',
    )
    search_fields = (
        'service_type',
        'month',
        'year',
    )
    ordering = ('-year', '-month', '-total_balance')
    readonly_fields = [field.name for field in UnsoldPaymentSummaryPeriod._meta.fields]
    list_per_page = 25

    def colored_service_type(self, obj):
        return format_html('<span style="color:#2c3e50;font-weight:500;">{}</span>', obj.service_type)
    colored_service_type.short_description = 'Service Type'

    def formatted_total_balance(self, obj):
        return f"{obj.total_balance:,.2f} ETB"
    formatted_total_balance.short_description = 'Total Balance'

    def has_add_permission(self, request):
        return False  # Prevent adding from admin

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion
    
@admin.register(CombinedBalanceSummary)
class CombinedBalanceSummaryAdmin(ImportExportModelAdmin):
    list_display = ('month', 'year', 'total_rent', 'total_sold_rent', 'total_unsold_rent', 'total_bill', 'total_sold_bill', 'total_unsold_bill', 'sold_transaction_count', 'unsold_customer_count')
    list_display_links = ('month', 'year', 'total_rent', 'total_sold_rent', 'total_unsold_rent', 'total_bill', 'total_sold_bill', 'total_unsold_bill', 'sold_transaction_count', 'unsold_customer_count')
    list_filter = ('year', 'month')
    search_fields = ('year',)
    ordering = ('-year', '-month')  # Show most recent first

    # Make the view read-only in admin
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(CombinedBalanceSummaryByService)
class CombinedBalanceSummaryByServiceAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'service_type',
        'month_year',
        'total_rent',
        'total_sold_rent',
        'total_unsold_rent',
        'total_bill',
        'total_sold_bill',
        'total_unsold_bill',
        'sold_transaction_count',
        'unsold_customer_count'
        )
    list_display_links = (
        'id',
        'service_type',
        'month_year',
        'total_rent',
        'total_sold_rent',
        'total_unsold_rent',
        'total_bill',
        'total_sold_bill',
        'total_unsold_bill',
        'sold_transaction_count',
        'unsold_customer_count'
    )
    list_filter = (
        'year',
        'month',
        'service_type',
    )
    search_fields = (
        'service_type',
        'year',
    )
    readonly_fields = (
        'service_type',
        'month',
        'year',
        'total_bill',
        'total_sold_bill',
        'total_unsold_bill',
        'sold_transaction_count',
        'unsold_customer_count',
    )

    def month_year(self, obj):
        return f"{obj.month}/{obj.year}"
    month_year.short_description = 'Period'
    month_year.admin_order_field = '-year'  # Allows sorting by year

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    # def monthly_report_link(self, obj):
    #     return format_html(
    #         '<a href="{}" target="_blank">Print Monthly Report</a>',
    #         reverse('print_combined_summary')
    #     )

    # monthly_report_link.short_description = "Print"
    # def colored_status(self, obj):
    #     """Highlight Employee Status in colors"""
    #     colors = {
    #         "active": "green",
    #         "inactive": "gray",
    #         "terminated": "red",
    #         "retired": "blue"
    #     }
    #     return format_html('<span style="color: {};">{}</span>', colors.get(obj.employee_status, "black"), obj.employee_status)
    
    # colored_status.admin_order_field = "employee_status"
    # colored_status.short_description = "Status"