from django.contrib import admin
from core.models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_key",
        "expire_date",
        "ip_address",
        "url_visited",
        "user_agent",
        "user_id",
        "updated_at",
    )
    list_filter = ("expire_date", "updated_at")
    search_fields = (
        "session_key",
        "user_id",
        "user_agent",
        "ip_address",
        "url_visited",
    )
    list_per_page = 50


# admin.site.register(Session, SessionAdmin)
# admin.site.register(User, UserAdmin)
