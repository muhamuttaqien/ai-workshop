import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mentor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("role", models.CharField(max_length=180)),
                ("bio", models.TextField()),
                ("photo", models.CharField(default="workshop/img/mentor.jpg", max_length=255)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("initials", models.CharField(max_length=4)),
                ("role", models.CharField(blank=True, max_length=180)),
                ("organization", models.CharField(blank=True, max_length=180)),
                ("quote", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="Workshop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("title", models.CharField(max_length=180)),
                ("headline", models.CharField(max_length=120)),
                ("headline_accent", models.CharField(max_length=120)),
                ("subtitle", models.CharField(blank=True, max_length=180)),
                ("description", models.TextField()),
                ("meta_description", models.CharField(blank=True, max_length=300)),
                ("layout_variant", models.CharField(choices=[("research", "Research"), ("productivity", "Productivity")], default="research", max_length=32)),
                ("eyebrow", models.CharField(default="AI WORKSHOP • ONLINE", max_length=80)),
                ("audience_label", models.CharField(blank=True, max_length=160)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("dates_label", models.CharField(max_length=120)),
                ("days_label", models.CharField(max_length=120)),
                ("time_label", models.CharField(max_length=80)),
                ("format_label", models.CharField(default="Online", max_length=80)),
                ("duration_label", models.CharField(default="Total 3 Jam", max_length=80)),
                ("price_label", models.CharField(blank=True, max_length=80)),
                ("registration_url", models.URLField(blank=True)),
                ("show_registration", models.BooleanField(default=True)),
                ("is_archived", models.BooleanField(default=False)),
                ("hero_image", models.CharField(blank=True, max_length=255)),
                ("hero_badge", models.CharField(blank=True, max_length=120)),
                ("hero_flow", models.CharField(blank=True, max_length=180)),
                ("hero_note", models.CharField(blank=True, max_length=180)),
                ("intro_title", models.CharField(max_length=220)),
                ("intro_paragraphs", models.JSONField(default=list)),
                ("outcomes", models.JSONField(default=list)),
                ("audience_title", models.CharField(max_length=220)),
                ("audience_intro", models.CharField(blank=True, max_length=300)),
                ("audiences", models.JSONField(default=list)),
                ("curriculum_title", models.CharField(max_length=220)),
                ("curriculum_intro", models.TextField(blank=True)),
                ("curriculum", models.JSONField(default=list)),
                ("benefits_title", models.CharField(default="Apa yang akan kamu dapatkan?", max_length=220)),
                ("benefits_intro", models.CharField(blank=True, max_length=300)),
                ("benefits", models.JSONField(default=list)),
                ("schedule_title", models.CharField(max_length=220)),
                ("schedule", models.JSONField(default=list)),
                ("mentor_section_title", models.CharField(max_length=220)),
                ("mentor_section_intro", models.TextField(blank=True)),
                ("registration_note", models.CharField(blank=True, max_length=220)),
                ("faqs", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("mentor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="workshops", to="workshop.mentor")),
            ],
            options={"ordering": ["-start_date"]},
        ),
    ]
