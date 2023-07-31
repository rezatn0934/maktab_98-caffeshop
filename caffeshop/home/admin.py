from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    readonly_fields = ["img_preview"]
    list_display = ["title", "img_preview", "is_active", ]
    list_editable = ["is_active"]