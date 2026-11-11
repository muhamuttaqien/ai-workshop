from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "tool_label", "level", "status", "is_published", "sort_order")
    list_editable = ("status", "is_published", "sort_order")
    list_filter = ("status", "level", "is_published")
    search_fields = ("title", "tool_label", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True

    fieldsets = (
        ("Informasi Kursus", {
            "fields": (
                "title", "slug", "tool_label", "short_description",
                "description", "audience", "learning_objectives",
            )
        }),
        ("Tampilan & Publikasi", {
            "fields": (
                ("level", "status"),
                "duration_label",
                ("is_published", "sort_order"),
            )
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    class Media:
        css = {"all": ("workshop/admin_titles.css",)}
