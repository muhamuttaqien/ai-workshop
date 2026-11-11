from django.db import models
from django.utils import timezone


class Mentor(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=180)
    bio = models.TextField()
    full_bio = models.TextField(
        blank=True,
        default="",
        help_text="Profil lengkap mentor yang ditampilkan saat kartu mentor dibuka.",
    )
    photo = models.CharField(
        max_length=255,
        default="workshop/img/mentor.jpg",
        help_text="Path file di static, contoh: workshop/img/mentor.jpg",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    initials = models.CharField(max_length=4)
    role = models.CharField(max_length=180, blank=True)
    organization = models.CharField(max_length=180, blank=True)
    quote = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


class Workshop(models.Model):
    LAYOUT_EDITORIAL = "editorial"
    LAYOUT_WORKFLOW = "workflow"
    LAYOUT_DASHBOARD = "dashboard"
    LAYOUT_SHOWCASE = "showcase"
    LAYOUT_GUIDE = "guide"
    LAYOUT_CHOICES = [
        (LAYOUT_EDITORIAL, "Editorial — Narrative & Knowledge"),
        (LAYOUT_WORKFLOW, "Workflow — Process & Hands-on"),
        (LAYOUT_DASHBOARD, "Dashboard — Data & Reporting"),
        (LAYOUT_SHOWCASE, "Showcase — Visual & Creative"),
        (LAYOUT_GUIDE, "Guide — Step-by-step & Beginner"),
    ]

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=180)
    headline = models.CharField(max_length=120)
    headline_accent = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=180, blank=True)
    description = models.TextField()
    meta_description = models.CharField(max_length=300, blank=True)

    layout_variant = models.CharField(
        max_length=32,
        choices=LAYOUT_CHOICES,
        default=LAYOUT_EDITORIAL,
        help_text=(
            "Pilih gaya halaman berdasarkan cara materi ingin dipresentasikan: "
            "Editorial, Workflow, Dashboard, Showcase, atau Guide."
        ),
    )
    eyebrow = models.CharField(max_length=80, default="AI WORKSHOP • ONLINE")
    audience_label = models.CharField(max_length=160, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()
    dates_label = models.CharField(max_length=120)
    days_label = models.CharField(max_length=120)
    time_label = models.CharField(max_length=80)
    format_label = models.CharField(max_length=80, default="Zoom Online")
    duration_label = models.CharField(
        max_length=120,
        default="2 Hari • Total 3 Jam (Live) + 6 Jam (Online)",
    )
    original_price_label = models.CharField(max_length=80, default="Rp780.000")
    price_label = models.CharField(max_length=80, default="Rp390.000")
    discount_label = models.CharField(max_length=40, default="50% OFF")

    registration_url = models.URLField(blank=True)
    show_registration = models.BooleanField(default=True)
    is_archived = models.BooleanField(
        default=False,
        help_text="Opsional. Workshop yang tanggal akhirnya sudah lewat otomatis diperlakukan sebagai workshop sebelumnya.",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Matikan saat masih menyiapkan draft. Workshop draft tidak muncul di website publik.",
    )

    hero_image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Path file di static, contoh: workshop/img/hero.jpg",
    )
    hero_badge = models.CharField(max_length=120, blank=True)
    hero_flow = models.CharField(max_length=180, blank=True)
    hero_note = models.CharField(max_length=180, blank=True)

    intro_title = models.CharField(max_length=220)

    audience_title = models.CharField(max_length=220)
    audience_intro = models.CharField(max_length=300, blank=True)

    curriculum_title = models.CharField(max_length=220)
    curriculum_intro = models.TextField(blank=True)

    benefits_title = models.CharField(max_length=220, default="Apa yang akan kamu dapatkan?")
    benefits_intro = models.CharField(max_length=300, blank=True)

    schedule_title = models.CharField(max_length=220)

    mentor = models.ForeignKey(Mentor, on_delete=models.PROTECT, related_name="workshops")
    mentor_section_title = models.CharField(max_length=220)
    mentor_section_intro = models.TextField(blank=True)

    registration_note = models.CharField(max_length=220, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    @property
    def has_ended(self):
        return self.is_archived or self.end_date < timezone.localdate()


class WorkshopIntroParagraph(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="intro_paragraph_items")
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.workshop.title}: intro {self.sort_order}"


class WorkshopOutcome(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="outcome_items")
    number = models.CharField(max_length=12, blank=True)
    title = models.CharField(max_length=160)
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class WorkshopAudience(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="audience_items")
    icon = models.CharField(max_length=12, blank=True)
    label = models.CharField(max_length=160)
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.label


class WorkshopCurriculumModule(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="curriculum_items")
    session_key = models.SlugField(
        max_length=80,
        help_text="Gunakan nilai yang sama untuk modul dalam sesi yang sama, contoh: day-01 atau session-01.",
    )
    session_label = models.CharField(max_length=80)
    session_title = models.CharField(max_length=220)
    session_day = models.CharField(max_length=80, blank=True)
    session_time = models.CharField(max_length=80, blank=True)
    number = models.CharField(max_length=12, blank=True)
    title = models.CharField(max_length=180)
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.session_label}: {self.title}"


class WorkshopBenefit(models.Model):
    VISUAL_LIVE = "live"
    VISUAL_PRACTICE = "practice"
    VISUAL_MATERIAL = "material"
    VISUAL_FLOW = "flow"
    VISUAL_REPLAY = "replay"
    VISUAL_MODULES = "modules"
    VISUAL_CHOICES = [
        (VISUAL_LIVE, "Live / 2 Hari"),
        (VISUAL_PRACTICE, "Hands-on / Interface"),
        (VISUAL_MATERIAL, "Materi / Document"),
        (VISUAL_FLOW, "Workflow"),
        (VISUAL_REPLAY, "Recording"),
        (VISUAL_MODULES, "12+ Modul"),
    ]

    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="benefit_items")
    number = models.CharField(max_length=12, blank=True)
    kicker = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=180)
    text = models.TextField()
    visual = models.CharField(max_length=24, choices=VISUAL_CHOICES, default=VISUAL_MATERIAL)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class WorkshopScheduleItem(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="schedule_items")
    number = models.CharField(max_length=12, blank=True)
    label = models.CharField(max_length=180)
    title = models.CharField(max_length=180)
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title


class WorkshopFAQ(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="faq_items")
    question = models.CharField(max_length=240)
    answer = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.question
