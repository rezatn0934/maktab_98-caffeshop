from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("phone", "first_name", "last_name", "is_staff", "is_active", "is_superuser",)
    list_filter = ("phone", "first_name", "last_name", "is_staff", "is_active", "is_superuser",)
    fieldsets = (
        (None, {"fields": ("phone", "password", "first_name", "last_name",)}),
        ("Permissions",
         {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone", "password1", "password2", "first_name", "last_name",
                "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("phone", 'first_name', 'last_name')
    ordering = ("phone",'first_name', 'last_name')


admin.site.site_header = 'Cafe Management'
admin.site.site_title = 'Coffee shop Management'
admin.site.index_title = 'Welcome to staff panel'
admin.site.register(User, CustomUserAdmin)
