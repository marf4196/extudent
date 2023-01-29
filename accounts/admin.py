from django.contrib import admin
from .models import User, Profile, UserIdentDocs
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ("email","phone_number")
    list_filter = ("email","phone_number", "is_active", "is_staff")
    ordering = ("-created_date",)
    list_display = ("phone_number", "is_active", "is_staff")
    fieldsets = (
        ("Authentication", {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        (
            "Group Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

admin.site.register(User, UserAdminConfig)
admin.site.register(Profile)
admin.site.register(UserIdentDocs)
