from django.contrib import admin
from .models import Order
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "date", "table_number", "total_price"]
    list_filter = ["phone_number", "date", "table_number", "total_price"]
    list_editable = ["phone_number", "table_number", "total_price"]

    search_fields = ["phone_number", "date", "table_number", "total_price"]
    ordering = ["phone_number", "date", "table_number", "total_price"]
    list_per_page = 15