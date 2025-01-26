from django.contrib import admin
from my_modules import UserAdmin
from .forms import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser
# _________________________________________________________________

class CustomUserAdmin(UserAdmin):
    fieldsets = (
            (None, {"fields": ("mobile_number", "password")}),
            (("Personal info"), {"fields": ("name", "family", "email")}),
            (
                ("Permissions"),
                {
                    "fields": (
                        "is_active",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    ),
                },
            ),
            # (("Important dates"), {"fields": ("last_login", "register_date")}),
        )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile_number", "password1", "password2"),
            },
        ),
    )
    
    list_display = ("mobile_number", "email", "name", "family","register_date","update_date")
    list_filter = ("is_active", "groups")
    search_fields = ("mobile_number","email")
    ordering = ("mobile_number",)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    
admin.site.register(CustomUser,CustomUserAdmin)
# _________________________________________________________________

