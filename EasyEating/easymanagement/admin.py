from django.contrib import admin

from .models import Business, EEUser, Order, OrderItem,Produce,ProduceStock,ProduceType,Desk

# Register your models here.


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display=("name","isActive","slug",)
    list_filter=("name","isActive")
    search_fields=("name",)
    

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display=("name","isReserve","isActive",)

@admin.register(EEUser)
class EEUserAdmin(admin.ModelAdmin):
    list_display=("username","is_manager")

@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display=("name","price",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("desk",)

@admin.register(ProduceType)
class ProduceTypeAdmin(admin.ModelAdmin):
    list_display=("name","business")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("get_desk", "produce", "quantity",)

    def get_desk(self, obj):
        return obj.order.desk

    get_desk.short_description = "Desk"