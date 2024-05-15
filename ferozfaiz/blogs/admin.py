from django.contrib import admin
from blogs.models import BlogPost

# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "status")
    search_fields = ("title", "author__username",
                     "author__first_name", "author__last_name", "content")
    list_filter = ("views", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at", "content_short")
    date_hierarchy = "created_at"
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20
    ordering = ("-updated_at",)
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "author")
        }),
        ("Content", {
            "fields": ("content", "content_short")
        }),
        ("Metadata", {
            # "fields": ("status", "tags")
            "fields": ("status", )
        }),
    )
    # filter_horizontal = ("tags",)
    raw_id_fields = ("author",)
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True
    list_select_related = ("author",)
    list_editable = ("status",)
    list_display_links = ("title",)
    list_per_page = 10
    list_max_show_all = 100
    list_display_links = ("title",)
