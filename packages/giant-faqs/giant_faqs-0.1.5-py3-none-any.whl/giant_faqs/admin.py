from django.contrib import admin

from . import models


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
   Admin class for editing FAQ objects
   """

    list_display = ["question", "category", "order", "is_active"]
    list_filter = ["category", "is_active"]
    list_editable = ["order"]
    search_fields = ["question"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["question", "answer", "category", "order", "is_active"]}),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]}),
    ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for editing FAQ category objects
    """

    list_display = ["name", "order"]
    list_editable = ["order"]
    search_fields = ["name"]
    field_set = [(None, {"fields": ["name", "order"]})]
