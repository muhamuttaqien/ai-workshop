from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [("courses", "0003_add_gemini_and_notebooklm_courses")]

    operations = [
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("slug", models.SlugField()),
                ("summary", models.CharField(blank=True, max_length=300)),
                ("content", models.TextField(help_text="Teks materi di bawah video. Gunakan baris kosong untuk paragraf baru.")),
                ("youtube_video_id", models.CharField(
                    blank=True, max_length=11,
                    validators=[django.core.validators.RegexValidator(regex="^[A-Za-z0-9_-]{11}$", message="Masukkan ID video YouTube 11 karakter.")],
                    help_text="Opsional. ID YouTube saja (11 karakter), bukan URL penuh. Video bisa ditambahkan kemudian.",
                )),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=False)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lessons", to="courses.course")),
            ],
            options={"ordering": ["sort_order", "pk"]},
        ),
        migrations.CreateModel(
            name="QuizQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.TextField()),
                ("option_a", models.CharField(max_length=250)),
                ("option_b", models.CharField(max_length=250)),
                ("option_c", models.CharField(max_length=250)),
                ("option_d", models.CharField(max_length=250)),
                ("correct_option", models.CharField(choices=[("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")], default="a", max_length=1)),
                ("explanation", models.TextField(blank=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_questions", to="courses.lesson")),
            ],
            options={"ordering": ["sort_order", "pk"]},
        ),
        migrations.AddConstraint(
            model_name="lesson",
            constraint=models.UniqueConstraint(fields=("course", "slug"), name="unique_course_lesson_slug"),
        ),
    ]
