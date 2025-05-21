from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.
class ComplainManagementAdmin(ImportExportModelAdmin):
    pass
    fieldsets = [
        ('General informations', {
            'fields': [('Category','Sub_category','Complain_type')],
        }),
		('Detail information', {
			'fields': [('Nature_of_complaint','Complain_details','Complain_related')],
		}),
    ]
    # fields = ['Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related']
    list_display = ['id','Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related','Complained_at','Updated_by','Registered_by']
    search_fields = ['id','Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related','Complained_at','Updated_by','Registered_by']
    list_filter = ['Category']
    list_display_links = ['id','Category','Sub_category','Complain_type','Nature_of_complaint','Complain_details','Complain_related','Complained_at','Updated_by','Registered_by']
    readonly_fields = ('id','Complained_at','Updated_by','Registered_by')
    list_per_page = 10
    list_select_related = True
    class Meta:
	    model = ComplainManagement	

    def save_model(self, request, obj, form, change):
	    if change:
		    obj.Update_by = request.user
		    obj.Complained_at = datetime.now()
	    obj.save()

admin.site.register(ComplainManagement, ComplainManagementAdmin)
