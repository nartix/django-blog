from django.contrib import admin
from users.models import User, UnverifiedUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "email2",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "email_verified",
        "is_staff",
        "is_superuser",
        "username_editable",
        "last_login",
        "date_joined",
        "password",
    )
    list_filter = ("is_active", "is_staff", "is_superuser",
                   "last_login", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(UnverifiedUser)
class UnverifiedUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "password",
        "last_login",
        "date_joined",
    )
    search_fields = ("username", "email")


# admin.site.register(Session, SessionAdmin)
# admin.site.register(User, UserAdmin)
