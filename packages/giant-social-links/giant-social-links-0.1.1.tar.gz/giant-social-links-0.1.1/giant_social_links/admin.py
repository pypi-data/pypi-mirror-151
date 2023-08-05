from django.contrib import admin

from giant_social_links import models


@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "order", "is_enabled"]
    list_editable = ["order", "is_enabled"]
    list_filter = ["is_enabled"]
    search_fields = ["name"]
    fieldsets = [
        (
            None,
            {"fields": ["name", "url", "icon", "order", "is_enabled"]},
        ),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]}),
    ]
    readonly_fields = ["created_at", "updated_at"]
