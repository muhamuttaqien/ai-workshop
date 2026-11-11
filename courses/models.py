from django.db import models
from django.core.validators import RegexValidator


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


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    slug = models.SlugField()
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField(help_text="Teks materi di bawah video. Gunakan baris kosong untuk paragraf baru.")
    youtube_video_id = models.CharField(
        max_length=11, blank=True,
        validators=[RegexValidator(regex=r"^[A-Za-z0-9_-]{11}$", message="Masukkan ID video YouTube 11 karakter.")],
        help_text="Opsional. ID YouTube saja (11 karakter), bukan URL penuh. Video bisa ditambahkan kemudian.",
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order", "pk"]
        constraints = [
            models.UniqueConstraint(fields=["course", "slug"], name="unique_course_lesson_slug"),
        ]

    def __str__(self):
        return f"{self.course.title} / {self.title}"


class QuizQuestion(models.Model):
    OPTIONS = [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")]

    lesson = models.ForeignKey(Lesson, related_name="quiz_questions", on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=250)
    option_b = models.CharField(max_length=250)
    option_c = models.CharField(max_length=250)
    option_d = models.CharField(max_length=250)
    correct_option = models.CharField(max_length=1, choices=OPTIONS, default="a")
    explanation = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]

    @property
    def choices(self):
        return [(key, getattr(self, "option_" + key)) for key in "abcd"]

    @property
    def correct_text(self):
        return getattr(self, "option_" + self.correct_option)

    def __str__(self):
        return self.question[:80]
