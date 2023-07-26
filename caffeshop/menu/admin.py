from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models import Count
from . import models
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
    list_display = ['name', 'category', 'price_per_item', 'active', 'num_product', 'description_product', 'img_preview']
    list_editable = ['category', 'price_per_item', 'active', 'num_product']
    list_filter = ['name', 'category', 'price_per_item', 'active', 'num_product']

    search_fields = ['name', 'category', 'price_per_item', 'active', 'num_product']
    ordering = ['name', 'category', 'price_per_item', 'active', 'num_product']
    list_per_page = 15


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'img_preview']
    list_filter = ['name']

    search_fields = ['name']
    ordering = ['name']
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
