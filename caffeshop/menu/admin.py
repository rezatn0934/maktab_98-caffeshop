
from django.contrib import admin
from django.db.models import Count
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    actions = ['delete_selected']
    readonly_fields = ['img_preview']

    list_display = [
        'name', 'category', 'price', 'order_count', 'is_active',
        'truncated_description', 'img_preview'
    ]
    list_editable = ['category', 'price', 'is_active']
    list_filter = ['name', 'category', 'price', 'is_active']
    search_fields = ['name__istartswith', 'category__name__istartswith']
    ordering = ['name', 'category', 'price', 'is_active']
    list_per_page = 15

    @admin.display(ordering='order_count')
    def order_count(self, product):
        url = (reverse('admin:orders_order_detail_changelist')
               + '?'
               + urlencode({
                    'product__id': str(product.id)
                }))

        return format_html('<a href="{}">{}</a>', url, product.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count('order_detail__product')
        )

    def truncated_description(self, obj):
        return truncatewords(obj.description, 10)

    truncated_description.short_description = 'Description'


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

    list_display = ['name', 'parent_category', 'product_count', 'img_preview']
    list_filter = ['name', 'parent_category']

    search_fields = ['name__istartswith', 'parent_category__name__istartswith']
    ordering = ['name', 'parent_category']
    list_per_page = 15

    @admin.display(ordering='product_count')
    def product_count(self, category):
        url = (reverse('admin:menu_product_changelist')
               + '?'
               + urlencode({
                    'category__id': str(category.id)
                }))

        return format_html('<a href="{}">{}</a>', url, category.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )

