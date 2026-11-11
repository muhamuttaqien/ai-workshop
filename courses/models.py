from django.db import models


class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Pemula"),
        ("intermediate", "Menengah"),
        ("advanced", "Lanjutan"),
    ]
    STATUS_CHOICES = [
        ("coming_soon", "Segera Hadir"),
        ("available", "Tersedia"),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    tool_label = models.CharField(max_length=80, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    audience = models.CharField(max_length=260, blank=True)
    learning_objectives = models.TextField(
        blank=True,
        help_text="Tulis satu tujuan pembelajaran per baris.",
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="beginner",
    )
    duration_label = models.CharField(max_length=80, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="coming_soon",
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Kursus draft tidak ditampilkan di website publik.",
    )
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title

    @property
    def objective_items(self):
        return [line.strip() for line in self.learning_objectives.splitlines() if line.strip()]
