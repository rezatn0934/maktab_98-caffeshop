from django.contrib import admin
from .models import Order, Order_detail
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


# Register your models here.


class OrderdetailInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.Order_detail
    min_num = 0
    max_num = 10
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

    inlines = [OrderdetailInline]
    list_display = ["id", "phone_number", "customer_count", "table_number", ]
    list_filter = ["phone_number", "table_number", "order_date", "last_modify", ]
    list_editable = ["table_number", ]

    search_fields = ["phone_number__istartswith", "table_number__istartswith"]
    ordering = ["phone_number", "order_date", "table_number", ]
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
    actions = ['delete_selected']

    autocomplete_fields = ['order_id', 'product']
    list_display = ["id", "order_id", "product", "quantity", "price",]

    list_filter = ["product", "quantity", "price",]
    list_editable = ["quantity", "price",]

    list_select_related = ['order']

    def order_id(self, obj):
        return obj.order.id

    search_fields = ["product__istartswith"]
    ordering = ["order_id", "product", "quantity", "price",]
    list_per_page = 15
