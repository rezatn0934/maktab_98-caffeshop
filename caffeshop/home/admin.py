from django.contrib import admin
from django.contrib.admin import site
from django.contrib import messages
from . import models


site.disable_action('delete_selected')

# Register your models here.

@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    readonly_fields = ["img_preview"]
    list_display = ["title", "img_preview", "is_active", ]
    list_editable = ["is_active"]


@admin.register(models.BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    readonly_fields = ["img_preview"]
    list_display = ["title", "img_preview", "is_active", ]
    list_editable = ["is_active"]
