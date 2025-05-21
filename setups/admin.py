from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

from django.contrib.contenttypes.models import ContentType

class OrganizationAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('name'), ('description'), 'status']
    list_display = ['id', 'name', 'description', 'status']
    search_fields = ['id', 'name', 'description', 'status']
    list_filter = ['name']
    list_display_links = ['id', 'name', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Organization

admin.site.register(Organization, OrganizationAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('organization'), ('name'),  ('description'), 'status']
    list_display = ['id', 'organization', 'name', 'description', 'status']
    search_fields = ['id', 'name', 'description', 'status']
    list_filter = ['name']
    list_display_links = ['id', 'organization', 'name', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Department

admin.site.register(Department, DepartmentAdmin)

class TaskAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('department'), ('name'),  ('description'), 'status']
    list_display = ['id', 'department', 'name', 'description', 'status']
    search_fields = ['id', 'name', 'description', 'status']
    list_filter = ['name']
    list_display_links = ['id', 'department', 'name', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Task

admin.site.register(Task, TaskAdmin)

class MeasurementAdmin(ImportExportModelAdmin):
    # pass
    fields = [('id'), ('name'), ('description'), 'value']
    list_display = ['id', 'name', 'description', 'value']
    search_fields = ['id', 'name', 'description', 'value']
    list_filter = ['name']
    list_display_links = ['id', 'name', 'description', 'value']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = Measurement

admin.site.register(Measurement, MeasurementAdmin)

class ItemListsAdmin(ImportExportModelAdmin):
    # pass
    fields = ['id', ('name'), ('description')]
    list_display = ['id', 'name', 'description']
    search_fields = ['id', 'name', 'description']
    list_filter = ['name']
    list_display_links = ['id', 'name', 'description']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = ItemLists

admin.site.register(ItemLists, ItemListsAdmin)

class MonthAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('month_amharic', 'month_english'), ('description'), 'status']
    list_display = ['id', 'month_amharic', 'month_english', 'description', 'status']
    search_fields = ['id', 'month_amharic', 'month_english', 'description', 'status']
    list_filter = ['month_english']
    list_display_links = ['id', 'month_amharic', 'month_english', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 12
    list_select_related = True

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    class Meta:
        model = Month

admin.site.register(Month, MonthAdmin)

class YearAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('year'), ('description'), 'status']
    list_display = ['id', 'year', 'description', 'status']
    search_fields = ['id', 'year', 'description', 'status']
    list_filter = ['year']
    list_display_links = ['id', 'year', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Year

admin.site.register(Year, YearAdmin)

class ZoneAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('reader'), ('zone'), ('description'), 'status']
    list_display = ['id', 'reader', 'zone', 'description', 'status']
    search_fields = ['id', 'reader', 'zone', 'description', 'status']
    list_filter = ['zone']
    list_display_links = ['id', 'reader', 'zone', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Zone

admin.site.register(Zone, ZoneAdmin)

class KebeleAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('kebele'), ('description'), 'status']
    list_display = ['id', 'kebele', 'description', 'status']
    search_fields = ['id', 'kebele', 'description', 'status']
    list_filter = ['kebele']
    list_display_links = ['id', 'kebele', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Kebele

admin.site.register(Kebele, KebeleAdmin)

class GaugeWidthAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('width'), ('description'), 'status']
    list_display = ['id', 'width', 'description', 'status']
    search_fields = ['id', 'width', 'description', 'status']
    list_filter = ['width']
    list_display_links = ['id', 'width', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = GaugeWidth

admin.site.register(GaugeWidth, GaugeWidthAdmin)

class ServiceTypeAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('service'), ('description'), 'status']
    list_display = ['id', 'service', 'description', 'status']
    search_fields = ['id', 'service', 'description', 'status']
    list_filter = ['service']
    list_display_links = ['id', 'service', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = ServiceType

admin.site.register(ServiceType, ServiceTypeAdmin)

class ServiceAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('name'), ('description'), 'status']
    list_display = ['id', 'name', 'description', 'status']
    search_fields = ['id', 'name', 'description', 'status']
    list_filter = ['name']
    list_display_links = ['id', 'name', 'description', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Service

admin.site.register(Service, ServiceAdmin)

class ServiceChargeAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('service_type'), ('service'), ('price'), 'status']
    list_display = ['id', 'service_type', 'service', 'price', 'status']
    search_fields = ['id', 'status']
    list_filter = ['service_type']
    list_display_links = ['id', 'service_type', 'service', 'price', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = ServiceCharge

admin.site.register(ServiceCharge, ServiceChargeAdmin)

class BlockAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('service_type'), ('name', 'value'), 'status']
    list_display = ['id', 'service_type', 'name', 'value', 'status']
    search_fields = ['id', 'service_type', 'name', 'value', 'status']
    list_filter = ['service_type']
    list_display_links = ['id', 'service_type', 'name', 'value', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Block

admin.site.register(Block, BlockAdmin)

class TariffAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('service_type'), ('min_consumption', 'max_consumption'), ('block1', 'block2'), ('block3', 'block4'), ('block5', 'status')]
    list_display = ['id', 'service_type', 'min_consumption', 'max_consumption', 'block1', 'block2', 'block3', 'block4', 'block5', 'status']
    search_fields = ['id', 'service_type']
    list_filter = ['service_type']
    list_display_links = ['id', 'service_type', 'min_consumption', 'max_consumption', 'block1', 'block2', 'block3', 'block4', 'block5', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Tariff

admin.site.register(Tariff, TariffAdmin)

class PenaltyAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('service_type'), ('name'), ('penalty', 'status')]
    list_display = ['id', 'service_type', 'name', 'penalty', 'status']
    search_fields = ['id', 'service_type', 'name', 'penalty', 'status']
    list_filter = ['service_type']
    list_display_links = ['id', 'service_type', 'name', 'penalty', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Penalty

admin.site.register(Penalty, PenaltyAdmin)

class ReaderAdmin(admin.ModelAdmin):
    # pass
    fields = [('id'), ('user'), ('name', 'status')]
    list_display = ['id', 'user', 'name', 'status']
    search_fields = ['id', 'user', 'name', 'status']
    list_filter = ['status']
    list_display_links = ['id', 'user', 'name', 'status']
    readonly_fields = ('id',)
    list_per_page = 10
    list_select_related = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    class Meta:
        model = Reader

admin.site.register(Reader, ReaderAdmin)

# @admin.register(BankType)
# class BankTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'code', 'status']
#     search_fields = ['name', 'code']
#     list_filter = ['status']
#     list_editable = ['status']
#     ordering = ['name']

# @admin.register(PaymentType)
# class PaymentTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'code', 'status']
#     search_fields = ['name', 'code']
#     list_filter = ['status']
#     list_editable = ['status']
#     ordering = ['name']
    
# @admin.register(BankPaymentType)
# class BankPaymentTypeAdmin(admin.ModelAdmin):
#     list_display = ['bank', 'payment_type', 'transaction_fee', 'is_active']
#     search_fields = ['bank__name', 'payment_type__name']
#     list_filter = ['is_active']
#     list_editable = ['is_active']
#     ordering = ['bank']