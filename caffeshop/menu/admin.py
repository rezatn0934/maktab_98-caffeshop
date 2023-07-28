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
    actions = ['deactivate_product']
    readonly_fields = ['img_preview']

    list_display = [
        'name', 'category', 'price_per_item', 'order_count', 'active', 'daily_availability',
        'truncated_description', 'img_preview'
    ]
    list_editable = ['category', 'price_per_item', 'active', 'daily_availability']
    list_filter = ['name', 'category', 'price_per_item', 'active', 'daily_availability']
    search_fields = ['name__istartswith', 'category__istartswith']
    ordering = ['name', 'category', 'price_per_item', 'active', 'daily_availability']
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

    @admin.action(description='deactivate products ')
    def deactivate_product(self, request, queryset):
        updated_count = queryset.update(active=False)
        self.message_user(
            request,
            f'{updated_count} products were successfully deactivated.',
        )

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'img_preview']
    list_filter = ['name']

    search_fields = ['name__istartswith']
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


@admin.register(models.ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_count', 'img_preview']
    list_filter = ['name']

    search_fields = ['name__istartswith']
    ordering = ['name']
    list_per_page = 15

    @admin.display(ordering='category_count')
    def category_count(self, parent_category):
        url = (reverse('admin:menu_category_changelist')
               + '?'
               + urlencode({
                    'parent_category__id': str(parent_category.id)
                }))

        return format_html('<a href="{}">{}</a>', url, parent_category.category_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            category_count=Count('category__parent_category')
        )