from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.utils import timezone

# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# from django.http import HttpResponse
# from reportlab.platypus import Paragraph

# def download_pdf(self, request, queryset):
#     # Getting the model name
#     model_name = self.model._meta.verbose_name_plural.title()

#     # Creating an HttpResponse object
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{model_name}.pdf"'

#     # Creating a PDF document
#     pdf = SimpleDocTemplate(response, pagesize=letter)
#     styles = getSampleStyleSheet()

#     # Adding a title to the PDF
#     title = styles['Title']
#     title_page = Paragraph(model_name, style=title)
#     pdf.build([title_page])

#     # Extracting headers and data from the queryset
#     headers = [field.verbose_name.title() for field in self.model._meta.fields]
#     data = [headers]

#     for obj in queryset:
#         data_row = [str(getattr(obj, field.name)) for field in self.model._meta.fields]
#         data.append(data_row)

#     # Creating a table and styling it
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))

#     # Adding the table to the PDF document
#     pdf.build([table])
    
#     return response

# # Correcting the function name
# download_pdf.short_description = 'Download selected items'

class StockManagementAdmin(ImportExportModelAdmin):
    fieldsets = [
        ('General information', {
            'fields': ['Name', 'Measurement', 'Quantity', 'Individual_price'],
        }),
        ('Detail information', {
            'fields': ['Total_price', 'Material_status'],
        }),
    ]
    list_display = ['id', 'Name', 'Measurement', 'Quantity', 'Individual_price', 'Total_price', 'Material_status', 'Registered_at', 'Updated_by', 'Registered_by']
    search_fields = ['id', 'Name', 'Measurement', 'Quantity', 'Individual_price', 'Total_price', 'Material_status', 'Registered_at', 'Updated_by', 'Registered_by']
    list_filter = ['Name__name', 'Measurement__name', 'Material_status']
    list_display_links = ['id', 'Name', 'Measurement', 'Quantity', 'Individual_price', 'Total_price', 'Material_status', 'Registered_at', 'Updated_by', 'Registered_by']
    readonly_fields = ('id', 'Total_price', 'Registered_at', 'Updated_by', 'Registered_by')
    list_per_page = 10
    list_select_related = True
    # actions = [download_pdf]

    def save_model(self, request, obj, form, change):
        if change:
            obj.Updated_by = request.user
        obj.Registered_at = timezone.now()
        obj.save()

admin.site.register(StockManagement, StockManagementAdmin)

class MaterialSaleReportAdmin(ImportExportModelAdmin):
    fieldsets = [
        ('General information', {
            'fields': ['NAME', 'QUANTITY', 'SINGLE_PRICE', 'TOTAL_PRICE'],
        }),
        ('Date information', {
            'fields': ['MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR'],
        }),
    ]
    list_display = ['ID', 'NAME', 'QUANTITY', 'SINGLE_PRICE', 'TOTAL_PRICE', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR']
    search_fields = ['ID', 'NAME', 'QUANTITY', 'SINGLE_PRICE', 'TOTAL_PRICE', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR']
    list_filter = ['MONTH_ENGLISH', 'YEAR']
    list_display_links = ['ID', 'NAME', 'QUANTITY', 'SINGLE_PRICE', 'TOTAL_PRICE', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR']
    readonly_fields = ('ID', 'NAME', 'QUANTITY', 'SINGLE_PRICE', 'TOTAL_PRICE', 'MONTH_AMHARIC', 'MONTH_ENGLISH', 'YEAR')
    list_per_page = 10
    list_select_related = True
    # actions = [download_pdf]

    def save_model(self, request, obj, form, change):
        if change:
            obj.Updated_by = request.user
        obj.Registered_at = timezone.now()
        obj.save()

admin.site.register(MaterialSaleReport, MaterialSaleReportAdmin)
