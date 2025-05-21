# admin.py
from django.contrib import admin
from .models import *
import logging
import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.timezone import now
from django.db import transaction
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import redirect
from django.db import connection
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import datetime
from datetime import datetime
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

import socket
from requests.exceptions import Timeout, ConnectionError
logger = logging.getLogger(__name__)

from django.contrib import messages 
from django.db import transaction
from collections import defaultdict

import csv
from io import StringIO

import concurrent.futures

from django.utils.html import format_html, mark_safe
from django.urls import reverse

# start
from django.urls import path
import json
from import_export import resources

# end

class BankBookAdmin(ImportExportModelAdmin):
	pass
	fields = [('id', 'Date'),('Deposite', 'Withdrawal'),('Balance'),('Registered_at','Updated_by','Registered_by')]
	list_display = ['id', 'Date', 'Deposite', 'Withdrawal', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	search_fields = ['id', 'Date', 'Deposite', 'Withdrawal', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	list_filter = ['Date']
	list_display_links = ['id', 'Date', 'Deposite', 'Withdrawal', 'Balance', 'Registered_at', 'Updated_by', 'Registered_by']
	readonly_fields = ('id','Balance','Registered_at','Updated_by','Registered_by')
	list_per_page = 10
	list_select_related = True
	class Meta:
		model = BankBook	

	def save_model(self, request, obj, form, change):
		if change:
			obj.Updated_by = request.user
			obj.Registered_at = datetime.now()
		obj.save()

admin.site.register(BankBook, BankBookAdmin) 
# Start
def export_and_send_bank_uploads(modeladmin, request, queryset):
    # Create a CSV in memory
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    # Write headers
    writer.writerow([
        'bill_id', 'bill_description', 'bill_reason', 'amount_due', 
        'customer_id', 'name', 'due_date', 'mobile', 'email',
        'Prev_Read', 'Curr_Read', 'Consumtion'
    ])
    
    # Write data rows
    for obj in queryset:
        writer.writerow([
            obj.bill_id, obj.bill_description, obj.bill_reason, str(obj.amount_due),
            obj.customer_id, obj.name, obj.due_date.strftime('%Y-%m-%d') if obj.due_date else '',
            obj.mobile, obj.email or '',
            str(obj.Prev_Read), str(obj.Curr_Read), str(obj.Consumtion)
        ])
    
    # Prepare the CSV content
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    
    # Prepare the API request
    api_url = 'http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/bulkBillUpload'
    api_key = 'AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE'
    
    try:
        # Create a temporary file-like object for the CSV
        files = {
            'uploadedFile': ('bank_uploads.csv', csv_content, 'text/csv')
        }
        
        headers = {
            'API_KEY': api_key
        }
        
        params = {
            'API_KEY': api_key
        }
        
        # Send the request
        response = requests.post(
            api_url,
            headers=headers,
            params=params,
            files=files
        )
        
        if response.status_code == 200:
            modeladmin.message_user(request, f"Successfully sent {queryset.count()} bills to banks", messages.SUCCESS)
        else:
            modeladmin.message_user(
                request, 
                f"Bank request failed with status {response.status_code}: {response.text}", 
                messages.ERROR
            )
    except Exception as e:
        modeladmin.message_user(request, f"Error sending bills to banks: {str(e)}", messages.ERROR)

export_and_send_bank_uploads.short_description = "Send bills to banks"

def export_and_cancel_bills(modeladmin, request, queryset):
    # Create a CSV in memory
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    # Write headers - confirm exact format with API documentation
    writer.writerow(['bill_id'])  # Some APIs may require different column names
    
    # Write data rows
    for obj in queryset:
        writer.writerow([obj.bill_id])
    
    # Get CSV content
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    
    # API configuration
    api_url = 'http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/bulkBillCancel'
    api_key = 'AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE'
    
    try:
        # Prepare request with explicit timeout
        files = {'uploadedFile': ('bills_to_cancel.csv', csv_content, 'text/csv')}
        headers = {'API_KEY': api_key}
        params = {'API_KEY': api_key}
        
        # Add these debugging steps:
        print(f"Attempting to send {queryset.count()} bills to cancellation API")
        print(f"Sample bill IDs: {[obj.bill_id for obj in queryset[:3]]}")
        
        # Send with timeout and verify=False if SSL issues exist
        response = requests.post(
            api_url,
            headers=headers,
            params=params,
            files=files,
            timeout=30,  # 30 seconds timeout
            verify=False  # Only if you have SSL certificate issues
        )
        
        # Debugging: Print raw response
        print(f"API Response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            modeladmin.message_user(
                request, 
                f"Successfully cancelled {queryset.count()} bills. Response: {response.text}",
                messages.SUCCESS
            )
        else:
            modeladmin.message_user(
                request, 
                f"API Error {response.status_code}: {response.text}", 
                messages.ERROR
            )
            
    except requests.exceptions.Timeout:
        modeladmin.message_user(
            request,
            "API request timed out after 30 seconds. Please try again later or contact support.",
            messages.ERROR
        )
    except requests.exceptions.SSLError:
        modeladmin.message_user(
            request,
            "SSL certificate verification failed. If this is expected, contact your administrator.",
            messages.ERROR
        )
    except Exception as e:
        modeladmin.message_user(
            request,
            f"Unexpected error: {str(e)}",
            messages.ERROR
        )
# End
class BankUploadResource(resources.ModelResource):
    class Meta:
        model = BankUpload
        exclude = ('month', 'year')
        import_id_fields = ['index']

@admin.register(BankUpload)
class BankRegistartionAdmin(ImportExportModelAdmin):
    resource_class = BankUploadResource
    list_display = (
        'index', 'bill_id', 'amount_due',
        'customer_id', 'name', 'due_date', 'mobile', 'email', 'month', 'year',
        'Prev_Read', 'Curr_Read', 'Consumtion'
    )
    list_display_links = ('index', 'bill_id', 'amount_due',
        'customer_id', 'name', 'due_date', 'mobile', 'email', 'month', 'year', 
        'Prev_Read', 'Curr_Read', 'Consumtion')
    search_fields = ('bill_id', 'name', 'bill_description')
    list_filter = ('month', 'year')

    # Optionally, you can make some fields readonly if necessary
    readonly_fields = ('index', 'bill_id', 'bill_description', 'bill_reason', 'amount_due')
    actions = [export_and_send_bank_uploads, export_and_cancel_bills]

    # ✅ Prevent delete from object view
    def has_delete_permission(self, request, obj=None):
        return False

    # ✅ Prevent delete from list actions
    def delete_model(self, request, obj):
        self.message_user(
            request,
            "You cannot delete records from this view.",
            level=messages.ERROR
        )

    def delete_queryset(self, request, queryset):
        self.message_user(
            request,
            "Bulk delete is not allowed. This data comes from a database view and is read-only.",
            level=messages.ERROR
        )

# class ItemInline(admin.TabularInline):
#     model = Item
#     extra = 1  # Allows adding at least one additional item inline
#     # Customize the form fields of the Item inline to make them more user-friendly
#     fields = ('name', 'price')
#     # Add some extra styling to the inline form in admin panel if necessary
#     classes = ['collapse']  # This will collapse the inline form initially to save space

# @admin.register(Bill)
# class BillAdmin(admin.ModelAdmin):
#     list_display = ('bill_id', 'full_name', 'customer_id', 'valid_until', 'status', 'phone_number')
#     search_fields = ['full_name', 'phone_number', 'bill_id', 'customer_id']
#     list_filter = ['status', 'valid_until']
#     inlines = [ItemInline]
#     actions = ['update_selected_bills']  # Add action option
#     readonly_fields = ('full_name', 'phone_number')  # Prevent editing these fields
#     fieldsets = (
#         (None, {
#             'fields': ('bill_id', 'valid_until', 'full_name', 'phone_number', 'status')
#         }),
#         ('Customer Info', {
#             'fields': ('customer_id',),
#             'classes': ('collapse',)  # Optionally collapse sections for clarity
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         """Saves the Bill instance without making an API request."""
#         super().save_model(request, obj, form, change)  # Save the model first

#     def update_selected_bills(self, request, queryset):
#         """Sends an update request to the provider API for selected bills."""
#         endpoint = "http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/updateOrRegisterBill"
#         api_key = "7264CBE3CED649E6BAA0D47669932E2B.ED1E0A2606AB4DA1B5E93AE779BFAD9C"
#         headers = {'Content-Type': 'application/json'}

#         for obj in queryset:
#             data = {
#                 "validUntil": str(obj.valid_until),
#                 "customer": {
#                     "fullName": obj.full_name,
#                     "phoneNumber": obj.phone_number,
#                     "customerId": obj.customer_id
#                 },
#                 "receiptData": {
#                     "items": [
#                         {"name": item.name, "price": float(item.price)}
#                         for item in obj.items.all()
#                     ]
#                 },
#                 "billId": obj.bill_id
#             }

#             try:
#                 response = requests.post(f"{endpoint}?API_KEY={api_key}", json=data, headers=headers)
#                 response.raise_for_status()  # Handle HTTP errors

#                 response_data = response.json() if response.headers.get('Content-Type') == 'application/json' else {}
#                 provider_status = response_data.get("responseStatus", {}).get("status")

#                 if provider_status is True:
#                     obj.status = "Success"
#                     messages.success(request, f"✅ Bill '{obj.bill_id}' updated successfully.")
#                 else:
#                     obj.status = "Not Success"
#                     messages.warning(request, f"⚠️ Failed to update bill '{obj.bill_id}'. Provider Response: {response_data}")

#             except requests.exceptions.RequestException as e:
#                 obj.status = "Not Success"
#                 error_msg = f"❌ Error updating bill '{obj.bill_id}': {str(e)}"
#                 logger.error(error_msg)
#                 messages.error(request, error_msg)

#             obj.save()  # Save the updated status

#     update_selected_bills.short_description = "Update selected bills in banks"

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponseRedirect
import requests
import logging

from .models import Bill, Item

logger = logging.getLogger(__name__)


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('valid_until', 'full_name', 'phone_number', 'customer_id', 'bill_id', 'status', 'sync_button')
    search_fields = ['full_name', 'phone_number']
    list_filter = ['status']
    inlines = [ItemInline]
    actions = ['sync_selected_bills']

    def sync_button(self, obj):
        return format_html('<a class="button" href="{}">🔄 Update</a>', f'sync/{obj.id}/')
    sync_button.short_description = 'Update Bill'
    sync_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync/<int:bill_id>/', self.admin_site.admin_view(self.sync_single_bill), name='sync-bill'),
        ]
        return custom_urls + urls

    def sync_single_bill(self, request, bill_id):
        try:
            bill = Bill.objects.get(id=bill_id)
            self.sync_bill_with_api(request, bill)
        except Bill.DoesNotExist:
            self.message_user(request, f"Bill with ID {bill_id} does not exist.", level=messages.ERROR)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

    @admin.action(description="🔄 Update selected bills")
    def sync_selected_bills(self, request, queryset):
        for bill in queryset:
            self.sync_bill_with_api(request, bill)

    def sync_bill_with_api(self, request, obj):
        endpoint = "http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/updateOrRegisterBill"
        api_key = "AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE"
        headers = {'Content-Type': 'application/json'}

        data = {
            "validUntil": str(obj.valid_until),
            "customer": {
                "fullName": obj.full_name,
                "phoneNumber": obj.phone_number,
                "customerId": obj.customer_id
            },
            "receiptData": {
                "items": [
                    {"name": item.name, "price": float(item.price)}
                    for item in obj.items.all()
                ]
            },
            "billId": obj.bill_id
        }

        try:
            response = requests.post(f"{endpoint}?API_KEY={api_key}", json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json() if response.headers.get('Content-Type') == 'application/json' else {}

            provider_status = response_data.get("responseStatus", {}).get("status")

            if provider_status is True:
                obj.status = "Success"
                messages.success(request, f"✅ Bill '{obj.bill_id}' updated successfully.")
            else:
                obj.status = "Not Success"
                messages.warning(request, f"⚠️ Failed to update bill '{obj.bill_id}'. Provider Response: {response_data}")

        except requests.exceptions.RequestException as e:
            obj.status = "Not Success"
            error_msg = f"❌ Error updating bill '{obj.bill_id}': {str(e)}"
            logger.error(error_msg)
            messages.error(request, error_msg)

        obj.save()

# admin.site.register(Item)

class BillSyncForm(forms.ModelForm):
    class Meta:
        model = BillSync
        fields = ['start_date', 'max', 'end_date']
        
@admin.register(BillSync)
class BillSyncAdmin(ImportExportModelAdmin):
    form = BillSyncForm
    list_display = ['start_date', 'end_date', 'status', 'sync_date', 'bill_id', 'paid_on', 'bank_name']
    search_fields = ['start_date', 'end_date']
    list_filter = ['status']
    list_display_links = ['start_date', 'end_date', 'status', 'sync_date']
    list_per_page = 10
    list_select_related = True

    actions = ['sync_bills']
    
    def sync_bills(self, request, queryset):
        endpoint = 'http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/billSync'
        api_key = 'AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE'
        headers = {'Content-Type': 'application/json'}

        successful_ids = []
        failed_ids = []

        try:
            with transaction.atomic():
                for sync in queryset:
                    try:
                        data = {
                            'startDate': str(sync.start_date),
                            'max': sync.max,
                            'endDate': str(sync.end_date)
                        }

                        logger.info(f"Syncing bills from {sync.start_date} to {sync.end_date}")

                        # Send the POST request to the API
                        response = requests.post(f"{endpoint}?API_KEY={api_key}", json=data, headers=headers)
                        response.raise_for_status()  # Raise exception for bad responses (4xx, 5xx)

                        if response.status_code == 200:
                            response_data = response.json()
                            if response_data:
                                for bill in response_data:
                                    # Create or update the BillSync record
                                    BillSync.objects.update_or_create(
                                        bill_id=bill["billId"],
                                        defaults={
                                            'start_date': sync.start_date,
                                            'end_date': sync.end_date,
                                            'paid_on': bill["paidOn"],
                                            'bank_transaction_reference': bill["bankTransactionReference"],
                                            'bank_name': bill["bankName"],
                                            'status': 'Completed',
                                        }
                                    )
                                successful_ids.append(sync.id)
                                logger.info(f"Bill sync from {sync.start_date} to {sync.end_date} succeeded.")
                            else:
                                failed_ids.append(sync.id)
                                logger.error(f"Bill sync failed from {sync.start_date} to {sync.end_date}: No data returned")
                        else:
                            failed_ids.append(sync.id)
                            logger.error(f"Sync request failed with status code {response.status_code} from {sync.start_date} to {sync.end_date}")

                    except requests.exceptions.RequestException as e:
                        logger.error(f"Error syncing bills from {sync.start_date} to {sync.end_date}: {e}")
                        failed_ids.append(sync.id)
                    except Exception as e:
                        logger.error(f"Unexpected error during sync from {sync.start_date} to {sync.end_date}: {e}")
                        failed_ids.append(sync.id)

                # Bulk update the status for all synced items
                if successful_ids:
                    queryset.filter(id__in=successful_ids).update(status='Success')
                if failed_ids:
                    queryset.filter(id__in=failed_ids).update(status='Not Success')

            # Provide summary feedback to the admin
            if successful_ids and failed_ids:
                self.message_user(request, f"Bill sync process completed. Success: {len(successful_ids)}, Failed: {len(failed_ids)}.", level='warning')
            elif successful_ids:
                self.message_user(request, "Bill sync process completed successfully.", level='success')
            elif failed_ids:
                self.message_user(request, "Bill sync process failed for all selected items.", level='error')

        except Exception as e:
            logger.error(f"Transaction failed during Bill sync: {e}")
            self.message_user(request, "Bill sync process encountered a critical error. Check the logs for details.", level='error')

    sync_bills.short_description = "Sync selected bills"

import logging

logger = logging.getLogger(__name__)

class BillSyncFileForm(forms.ModelForm):
    class Meta:
        model = BillSyncFile
        fields = ['start_date', 'end_date']  # No file field, since it's auto-fetched

@admin.register(BillSyncFile)
class BillSyncFileAdmin(admin.ModelAdmin):
    form = BillSyncFileForm
    list_display = ['downloaded_file', 'start_date', 'end_date', 'status', 'download_date']
    search_fields = ['start_date', 'end_date']
    list_filter = ['status']
    list_display_links = ['downloaded_file', 'start_date', 'end_date', 'status', 'download_date']
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        """Fetch the CSV from API and save it when a new record is created."""
        super().save_model(request, obj, form, change)

        if not change:  # Only fetch the file when a new record is added
            try:
                self.fetch_and_save_file(obj)  # Pass the instance (obj)
                self.message_user(request, f"File successfully fetched and saved for {obj.start_date} - {obj.end_date}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch file for {obj}: {e}")
                self.message_user(request, f"Failed to fetch file for {obj.start_date} - {obj.end_date}", level='error')

    def fetch_and_save_file(self, obj):
        """Fetch the file from the external API and save it."""
        API_URL = "http://196.189.53.130:28080/enterprise_dir/d0f3883b-9de7-4565-a7d2-b13ae67ca99d.csv"
        API_KEY = "AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE"

        params = {"startDate": str(obj.start_date), "endDate": str(obj.end_date)}
        headers = {"API_KEY": API_KEY}

        try:
            response = requests.get(API_URL, headers=headers, params=params)

            if response.status_code == 200 and response.content:
                # Generate a unique filename based on the date range
                file_name = f"sync_file_{obj.start_date}_{obj.end_date}.csv"
                # Save the file to the model's FileField
                obj.downloaded_file.save(file_name, ContentFile(response.content))
                obj.status = "Success"
                logger.info(f"✅ File successfully saved: {file_name}")
            else:
                obj.status = "Not Success"
                logger.warning(f"⚠ No content received for {obj.start_date} - {obj.end_date}")

        except requests.exceptions.RequestException as e:
            obj.status = "Error"
            logger.error(f"❌ Error fetching file: {e}")

        obj.save()

class BillCancellationForm(forms.ModelForm):
    class Meta:
        model = BillCancellation
        fields = ['bill_id']

@admin.register(BillCancellation)
class BillCancellationAdmin(admin.ModelAdmin):
    form = BillCancellationForm
    list_display = ['bill_id', 'status', 'cancel_date']
    search_fields = ['bill_id']
    list_filter = ['status']
    list_per_page = 10
    actions = ['cancel_selected_bills']

    def cancel_selected_bills(self, request, queryset):
        """
        Cancels selected bills with improved success detection
        """
        base_url = 'http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/cancelBill'
        api_key = 'AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE'

        for cancel_request in queryset:
            url = f"{base_url}?API_KEY={api_key}&bill_id={cancel_request.bill_id}"
            
            try:
                response = requests.post(
                    url,
                    headers={
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    data='',
                    timeout=10
                )

                logger.info(f"Cancellation response for {cancel_request.bill_id}: {response.status_code} - {response.text}")

                # Handle successful cancellation (200 status code)
                if response.status_code == 200:
                    cancel_request.status = 'Success'
                    cancel_request.cancel_date = timezone.now()
                    cancel_request.save()
                    
                    # Try to get detailed success message
                    try:
                        response_data = response.json()
                        if response_data.get('status') is True:
                            messages.success(request, f"✅ Successfully canceled bill {cancel_request.bill_id}")
                        else:
                            messages.success(request, f"✅ Cancellation processed for bill {cancel_request.bill_id} (API returned non-true status)")
                    except ValueError:
                        if 'success' in response.text.lower():
                            messages.success(request, f"✅ Successfully canceled bill {cancel_request.bill_id}")
                        else:
                            messages.success(request, f"✅ Cancellation processed for bill {cancel_request.bill_id} (unexpected response format)")

                # Handle other status codes
                else:
                    cancel_request.status = 'Failed'
                    cancel_request.save()
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('message', response.text)
                    except ValueError:
                        error_msg = response.text
                    messages.error(request, f"❌ Failed to cancel bill {cancel_request.bill_id}: {error_msg}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for {cancel_request.bill_id}: {str(e)}")
                cancel_request.status = 'Failed'
                cancel_request.save()
                messages.error(request, f"❌ Connection error while canceling bill {cancel_request.bill_id}: {str(e)}")

        messages.info(request, f"Completed processing {queryset.count()} bill cancellation(s)")
    
# @admin.register(BulkBillUpload)
# class BulkBillUploadAdmin(admin.ModelAdmin):
#     list_display = ('id', 'file', 'status', 'created_at', 'updated_at')
#     list_display_links = ('id', 'file', 'status', 'created_at', 'updated_at')
#     list_filter = ('status',)
#     readonly_fields = ('status', 'error_message', 'created_at', 'updated_at')
#     actions = ['process_upload']
    
#     def process_upload(self, request, queryset):
#         if queryset.count() != 1:
#             self.message_user(request, "Please select exactly one record to process.", level='error')
#             return
        
#         upload = queryset.first()
        
#         try:
#             # Prepare the file for upload
#             files = {'uploadedFile': upload.file.open('rb')}
            
#             # API endpoint and key
#             url = "http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/bulkBillUpload"
#             api_key = "7264CBE3CED649E6BAA0D47669932E2B.ED1E0A2606AB4DA1B5E93AE779BFAD9C"
            
#             # Make the POST request
#             response = requests.post(
#                 f"{url}?API_KEY={api_key}",
#                 files=files
#             )
            
#             # Close the file
#             files['uploadedFile'].close()
            
#             # Update the model based on response
#             if response.status_code == 200:
#                 upload.status = 'success'
#                 upload.error_message = ''
#                 upload.save()
#                 self.message_user(request, "File uploaded successfully!")
#             else:
#                 upload.status = 'failed'
#                 upload.error_message = f"API returned status code: {response.status_code}"
#                 upload.save()
#                 self.message_user(request, f"Upload failed with status code: {response.status_code}", level='error')
                
#         except Exception as e:
#             upload.status = 'failed'
#             upload.error_message = str(e)
#             upload.save()
#             self.message_user(request, f"Error: {str(e)}", level='error')
            
#         return HttpResponseRedirect(reverse('admin:bill_upload_bulkbillupload_changelist'))
    
#     process_upload.short_description = "Process selected upload to API"

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from .models import BulkBillUpload

@admin.register(BulkBillUpload)
class BulkBillUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'status', 'created_at', 'updated_at')
    list_display_links = ('id', 'file', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    readonly_fields = ('status', 'error_message', 'created_at', 'updated_at')
    actions = ['process_upload']
    
    def process_upload(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one record to process.", level='error')
            return
        
        upload = queryset.first()
        
        try:
            # Prepare the file for upload
            files = {'uploadedFile': upload.file.open('rb')}
            
            # API endpoint and key
            url = "http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/bulkBillUpload"
            api_key = "AF7E9EDA54244A8B9E7CAF383657DBDF.26F252A550D44A9580BF7B91BEB390AE"
            
            # Make the POST request
            response = requests.post(
                f"{url}?API_KEY={api_key}",
                files=files
            )
            
            # Close the file
            files['uploadedFile'].close()
            
            # Update the model based on response
            if response.status_code == 200:
                upload.status = 'success'
                upload.error_message = ''
                upload.save()
                self.message_user(request, "File uploaded successfully!")
            else:
                upload.status = 'failed'
                upload.error_message = f"API returned status code: {response.status_code}"
                upload.save()
                self.message_user(request, f"Upload failed with status code: {response.status_code}", level='error')
                
        except Exception as e:
            upload.status = 'failed'
            upload.error_message = str(e)
            upload.save()
            self.message_user(request, f"Error: {str(e)}", level='error')
            
        # Redirect back to the changelist page
        opts = self.model._meta
        return HttpResponseRedirect(reverse(f'admin:{opts.app_label}_{opts.model_name}_changelist'))
    
    process_upload.short_description = "Upload bills to banks"