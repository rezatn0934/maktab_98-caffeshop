from django.contrib import admin
from . import models
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
    list_display = ['name', 'category', 'price_per_item', 'active', 'num_product', 'description_product', 'img_preview']
    list_editable = ['category', 'price_per_item', 'active', 'num_product']
    list_filter = ['name', 'category', 'price_per_item', 'active', 'num_product']

    search_fields = ['name', 'category', 'price_per_item', 'active', 'num_product']
    ordering = ['name', 'category', 'price_per_item', 'active', 'num_product']
    list_per_page = 15
