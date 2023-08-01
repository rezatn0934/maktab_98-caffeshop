from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.contrib.admin import site
from django.contrib import messages
from . import models

site.disable_action('delete_selected')


# Register your models here.

@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    readonly_fields = ["img_preview"]
    list_display = ["title", "img_preview", "is_active", ]
    list_editable = ["is_active"]


@admin.register(models.BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    actions = ['delete_background_image']
    readonly_fields = ["img_preview"]
    list_display = ["title", "img_preview", "is_active", ]
    list_editable = ["is_active"]

    @admin.action(description='Delete selected background images ')
    def delete_background_image(self, request, queryset):
        count = 0
        for query in queryset:
            if query.is_active:
                self.message_user(
                    request,
                    f'{query.title} Background image can not be deleted.',
                    messages.ERROR,
                )
            else:
                count += 1
                query.delete()

        if count:
            self.message_user(
                request,
                f'{count} selected background images were successfully deleted.',
            )


@admin.register(models.Info)
class InfoAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
    list_display = ["phone", "email", "work_hours", "address", "instagram", "facebook", "twitter"]


@admin.register(models.Logo)
class InfoAdmin(admin.ModelAdmin):
    actions = ['delete_logo_image']
    readonly_fields = ["img_preview"]
    list_display = ["title", "img_preview", "is_active", ]
    list_editable = ["is_active"]

    @admin.action(description='Delete selected logo  ')
    def delete_logo_image(self, request, queryset):
        count = 0
        for query in queryset:
            if query.is_active:
                self.message_user(
                    request,
                    f'{query.title} logo can not be deleted.',
                    messages.ERROR,
                )
            else:
                count += 1
                query.delete()

        if count:
            self.message_user(
                request,
                f'{count} selected logo were successfully deleted.',
            )


@admin.register(models.About)
class AboutAdmin(admin.ModelAdmin):
    actions = ['delete_about_image']
    readonly_fields = ['img_preview']
    list_display = ['title', 'truncated_content', 'img_preview', 'is_active', ]
    list_editable = ['is_active']

    @admin.action(description='Delete selected about  ')
    def delete_about_image(self, request, queryset):
        count = 0
        for query in queryset:
            if query.is_active:
                self.message_user(
                    request,
                    f'{query.title} about can not be deleted.',
                    messages.ERROR,
                )
            else:
                count += 1
                query.delete()

        if count:
            self.message_user(
                request,
                f'{count} selected about were successfully deleted.',
            )

    def truncated_content(self, obj):
        return truncatewords(obj.content, 10)

    truncated_content.short_description = 'Content'
