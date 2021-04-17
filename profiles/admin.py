from django.contrib import admin
from .models import Patient, Doctor


# from import_export import resources
# from import_export.admin import ImportExportModelAdmin


# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'departmentID', 'dob', 'sex', 'address')
    list_per_page = 20
