from django.contrib import admin, messages
from django.utils.text import slugify

from .models import (
    Mentor,
    Testimonial,
    Workshop,
    WorkshopAudience,
    WorkshopBenefit,
    WorkshopCurriculumModule,
    WorkshopFAQ,
    WorkshopIntroParagraph,
    WorkshopOutcome,
    WorkshopScheduleItem,
)


class SortableInlineMixin:
    extra = 0
    ordering = ("sort_order", "id")
    classes = ("collapse",)


class IntroParagraphInline(SortableInlineMixin, admin.TabularInline):
    model = WorkshopIntroParagraph
    fields = ("text", "sort_order")
    verbose_name = "Paragraf intro"
    verbose_name_plural = "Tentang workshop: paragraf intro"


class OutcomeInline(SortableInlineMixin, admin.StackedInline):
    model = WorkshopOutcome
    fields = (("number", "sort_order"), "title", "text")
    verbose_name = "Outcome"
    verbose_name_plural = "Tentang workshop: outcome"


class AudienceInline(SortableInlineMixin, admin.StackedInline):
    model = WorkshopAudience
    fields = (("icon", "sort_order"), "label", "text")
    verbose_name = "Target peserta"
    verbose_name_plural = "Target peserta"


class CurriculumModuleInline(SortableInlineMixin, admin.StackedInline):
    model = WorkshopCurriculumModule
    fields = (
        ("session_key", "sort_order"),
        ("session_label", "session_day", "session_time"),
        "session_title",
        ("number", "title"),
        "text",
    )
    verbose_name = "Modul materi"
    verbose_name_plural = "Materi workshop (urutkan semua modul dengan Sort order)"


class BenefitInline(SortableInlineMixin, admin.StackedInline):
    model = WorkshopBenefit
    fields = (("number", "kicker", "visual", "sort_order"), "title", "text")
    verbose_name = "Benefit"
    verbose_name_plural = "Benefit & fasilitas"


class ScheduleInline(SortableInlineMixin, admin.StackedInline):
    model = WorkshopScheduleItem
    fields = (("number", "sort_order"), "label", "title", "text")
    verbose_name = "Sesi jadwal"
    verbose_name_plural = "Jadwal sesi"


class FAQInline(SortableInlineMixin, admin.StackedInline):
    model = WorkshopFAQ
    fields = (("sort_order",), "question", "answer")
    verbose_name = "FAQ"
    verbose_name_plural = "FAQ"


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    search_fields = ("name", "role", "bio", "full_bio")
    fields = ("name", "role", "photo", "bio", "full_bio")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "organization", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "organization", "quote")


@admin.action(description="Duplicate workshop terpilih sebagai draft")
def duplicate_workshops(modeladmin, request, queryset):
    created = 0

    child_relations = [
        ("intro_paragraph_items", WorkshopIntroParagraph),
        ("outcome_items", WorkshopOutcome),
        ("audience_items", WorkshopAudience),
        ("curriculum_items", WorkshopCurriculumModule),
        ("benefit_items", WorkshopBenefit),
        ("schedule_items", WorkshopScheduleItem),
        ("faq_items", WorkshopFAQ),
    ]

    for workshop in queryset.select_related("mentor"):
        values = {}
        for field in Workshop._meta.fields:
            if field.primary_key or field.name in {"created_at", "updated_at"}:
                continue
            values[field.name] = getattr(workshop, field.name)

        base_slug = slugify(f"{workshop.slug}-copy") or "workshop-copy"
        slug = base_slug
        counter = 2
        while Workshop.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        values["title"] = f"{workshop.title} (Copy)"
        values["slug"] = slug
        values["is_published"] = False
        values["is_archived"] = False
        values["show_registration"] = False
        values["registration_url"] = ""

        clone = Workshop.objects.create(**values)

        for related_name, model in child_relations:
            for child in getattr(workshop, related_name).all():
                child_values = {}
                for field in model._meta.fields:
                    if field.primary_key or field.name == "workshop":
                        continue
                    child_values[field.name] = getattr(child, field.name)
                model.objects.create(workshop=clone, **child_values)

        created += 1

    modeladmin.message_user(
        request,
        f"{created} workshop berhasil diduplikasi sebagai draft. Ubah judul, tanggal, dan konten lalu aktifkan Published.",
        level=messages.SUCCESS,
    )


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_date",
        "end_date",
        "layout_variant",
        "is_published",
        "show_registration",
        "is_archived",
    )
    list_editable = ("is_published", "show_registration", "is_archived")
    list_filter = ("layout_variant", "is_published", "show_registration", "is_archived")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("mentor",)
    date_hierarchy = "start_date"
    save_on_top = True
    actions = (duplicate_workshops,)

    fieldsets = (
        (
            "01. Identitas & Tampilan",
            {
                "fields": (
                    "title",
                    "slug",
                    ("headline", "headline_accent"),
                    "subtitle",
                    "description",
                    "meta_description",
                    "layout_variant",
                    "eyebrow",
                    "audience_label",
                )
            },
        ),
        (
            "02. Publikasi, Jadwal & Pendaftaran",
            {
                "fields": (
                    ("is_published", "is_archived"),
                    ("start_date", "end_date"),
                    "dates_label",
                    "days_label",
                    "time_label",
                    ("format_label", "duration_label"),
                    ("original_price_label", "price_label", "discount_label"),
                    "registration_url",
                    "show_registration",
                    "registration_note",
                )
            },
        ),
        (
            "03. Hero",
            {
                "fields": ("hero_image", "hero_badge", "hero_flow", "hero_note"),
                "classes": ("collapse",),
            },
        ),
        (
            "04. Judul Section",
            {
                "fields": (
                    "intro_title",
                    "audience_title",
                    "audience_intro",
                    "curriculum_title",
                    "curriculum_intro",
                    "benefits_title",
                    "benefits_intro",
                    "schedule_title",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "05. Mentor",
            {
                "fields": ("mentor", "mentor_section_title", "mentor_section_intro"),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    inlines = (
        IntroParagraphInline,
        OutcomeInline,
        AudienceInline,
        CurriculumModuleInline,
        BenefitInline,
        ScheduleInline,
        FAQInline,
    )
