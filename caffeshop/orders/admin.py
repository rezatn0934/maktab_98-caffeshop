from django.contrib import admin
from .models import Order, Order_detail
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "date", "table_number", "total_price"]
    list_filter = ["phone_number", "date", "table_number", "total_price"]
    list_editable = ["phone_number", "table_number", "total_price"]

    search_fields = ["phone_number", "date", "table_number", "total_price"]
    ordering = ["phone_number", "date", "table_number", "total_price"]
    list_per_page = 15


@admin.register(Order_detail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "product", "quantity", "price", "total_price"]

    list_filter = ["product", "quantity", "price", "total_price"]
    list_editable = ["product", "quantity", "price", "total_price"]
    list_select_related = ['order']

    def order_id(self, obj):
        return obj.order.id

    search_fields = ["product", "quantity", "price", "total_price"]
    ordering = ["order_id", "product", "quantity", "price", "total_price"]
    list_per_page = 15
