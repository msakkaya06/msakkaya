from django.contrib import admin
from .models import Computer_Informations, InfoCard, PrinterScannerInformation, TebsGroup, TebsUser, Unit


@admin.register(InfoCard)
class InfoCardAdmin(admin.ModelAdmin):
    list_display=("title","description","isActive","date",)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display=("name","parent_unit")

@admin.register(TebsUser)
class TebsUserAdmin(admin.ModelAdmin):
    list_display=("username","first_name","last_name",)

@admin.register(Computer_Informations)
class Computer_InformationsAdmin(admin.ModelAdmin):
    list_display=("computer_name","manufacturer","model",)

@admin.register(TebsGroup)
class TebsGroup_Admin(admin.ModelAdmin):
    list_display=("original_group","display_name",)

@admin.register(PrinterScannerInformation)
class PrinterScannerInformation_Admin(admin.ModelAdmin):
    list_display=("device_name","device_type","manufacturer")
# Register your models here.

# Register your models here.
