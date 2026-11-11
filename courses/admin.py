from django.contrib import admin

from .models import Course, Lesson, QuizQuestion


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ("title", "slug", "sort_order", "is_published")
    show_change_link = True


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 0
    fields = (
        "question", ("option_a", "option_b"), ("option_c", "option_d"),
        "correct_option", "explanation", "sort_order",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline,)
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


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "sort_order", "is_published")
    list_filter = ("is_published", "course")
    list_editable = ("sort_order", "is_published")
    search_fields = ("title", "course__title")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (QuizQuestionInline,)
    fieldsets = (
        ("Informasi Lesson", {"fields": ("course", "title", "slug", "summary")}),
        ("Materi", {"fields": ("youtube_video_id", "content")}),
        ("Publikasi", {"fields": ("sort_order", "is_published")}),
    )

    class Media:
        css = {"all": ("workshop/admin_titles.css",)}
