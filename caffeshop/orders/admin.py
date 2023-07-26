from django.contrib import admin
from .models import Order, Order_detail
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "customer_count", "table_number", "total_price"]
    list_filter = ["phone_number", "date", "table_number", "total_price"]
    list_editable = ["phone_number", "table_number", "total_price"]

    search_fields = ["phone_number__istartswith", "table_number__istartswith"]
    ordering = ["phone_number", "date", "table_number", "total_price"]
    list_per_page = 15

    def customer_count(self, obj):
        url = (reverse('admin:orders_order_detail_changelist')
               + '?'
               + urlencode({
                    'order__id': str(obj.id)
                }))
        return format_html('<a href="{}">{}</a>', url, obj.customer_count)

    customer_count.short_description = 'Number of Orders'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(customer_count=Count('order_detail__order'))

    customer_count.admin_order_field = 'customer_count'




@admin.register(Order_detail)
class OrderDetailAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order_id', 'product']
    list_display = ["id", "order_id", "product", "quantity", "price", "total_price"]

    list_filter = ["product", "quantity", "price", "total_price"]
    list_editable = ["quantity", "price", "total_price"]
    list_select_related = ['order']

    def order_id(self, obj):
        return obj.order.id

    search_fields = ["product__istartswith"]
    ordering = ["order_id", "product", "quantity", "price", "total_price"]
    list_per_page = 15
