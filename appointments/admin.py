from django.contrib import admin
from .models import Appointment
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin


# Register your models here.
# class AppointmentResource(resources.ModelResource):
#     class Meta:
#         model = Appointment

#
# @admin.register(Appointment)
# class AppointmentReAdmin(ImportExportModelAdmin):
#     resource_class = AppointmentResource
#     list_display = ('id', 'doctor', 'patient', 'appointment_time')
#     #list_filter = ('appt_access')
#     search_fields = ('patient', 'doctor')
#     list_per_page = 20

# admin.site.register(Appointment, AppointmentAdmin)
