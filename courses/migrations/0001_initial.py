from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("slug", models.SlugField(unique=True)),
                ("tool_label", models.CharField(blank=True, max_length=80)),
                ("short_description", models.CharField(max_length=300)),
                ("description", models.TextField()),
                ("audience", models.CharField(blank=True, max_length=260)),
                ("learning_objectives", models.TextField(blank=True, help_text="Tulis satu tujuan pembelajaran per baris.")),
                ("level", models.CharField(choices=[("beginner", "Pemula"), ("intermediate", "Menengah"), ("advanced", "Lanjutan")], default="beginner", max_length=20)),
                ("duration_label", models.CharField(blank=True, max_length=80)),
                ("status", models.CharField(choices=[("coming_soon", "Segera Hadir"), ("available", "Tersedia")], default="coming_soon", max_length=20)),
                ("is_published", models.BooleanField(default=False, help_text="Kursus draft tidak ditampilkan di website publik.")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["sort_order", "title"]},
        ),
    ]
