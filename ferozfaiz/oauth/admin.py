from django.contrib import admin
from .models import OAuthProvider, OAuthUser


@admin.register(OAuthProvider)
class OAuthProviderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "client_id",
        "authorization_base_url",
        "token_url",
        "scope",
        "profile_url",
    )
    search_fields = ("name",)


@admin.register(OAuthUser)
class OAuthUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "provider",
        "uid",
        "email",
        "expires_in",
        "date_joined",
        "last_login",
    )
    # form fields
    # fields = (
    #     "user",
    #     "provider",
    #     "uid",
    #     "email",
    #     "access_token",
    #     "refresh_token",
    #     "expires_in",
    #     "profile_data",
    #     "date_joined",
    #     "last_login",
    # )
    search_fields = ("user__username", "provider__name", "uid", "email")
