import django.db.models.deletion
from django.db import migrations, models


def migrate_json_to_relations(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Intro = apps.get_model("workshop", "WorkshopIntroParagraph")
    Outcome = apps.get_model("workshop", "WorkshopOutcome")
    Audience = apps.get_model("workshop", "WorkshopAudience")
    Curriculum = apps.get_model("workshop", "WorkshopCurriculumModule")
    Benefit = apps.get_model("workshop", "WorkshopBenefit")
    Schedule = apps.get_model("workshop", "WorkshopScheduleItem")
    FAQ = apps.get_model("workshop", "WorkshopFAQ")

    for workshop in Workshop.objects.all():
        for idx, text in enumerate(workshop.intro_paragraphs or [], start=1):
            Intro.objects.create(workshop=workshop, text=text, sort_order=idx)

        for idx, item in enumerate(workshop.outcomes or [], start=1):
            Outcome.objects.create(
                workshop=workshop,
                number=item.get("number", ""),
                title=item.get("title", ""),
                text=item.get("text", ""),
                sort_order=idx,
            )

        for idx, item in enumerate(workshop.audiences or [], start=1):
            Audience.objects.create(
                workshop=workshop,
                icon=item.get("icon", ""),
                label=item.get("label", ""),
                text=item.get("text", ""),
                sort_order=idx,
            )

        module_order = 1
        for session_index, session in enumerate(workshop.curriculum or [], start=1):
            session_key = f"session-{session_index:02d}"
            for module in session.get("modules", []):
                Curriculum.objects.create(
                    workshop=workshop,
                    session_key=session_key,
                    session_label=session.get("label", ""),
                    session_title=session.get("title", ""),
                    session_day=session.get("day", ""),
                    session_time=session.get("time", ""),
                    number=module.get("number", ""),
                    title=module.get("title", ""),
                    text=module.get("text", ""),
                    sort_order=module_order,
                )
                module_order += 1

        for idx, item in enumerate(workshop.benefits or [], start=1):
            Benefit.objects.create(
                workshop=workshop,
                number=item.get("number", ""),
                kicker=item.get("kicker", ""),
                title=item.get("title", ""),
                text=item.get("text", ""),
                visual=item.get("visual", "material"),
                sort_order=idx,
            )

        for idx, item in enumerate(workshop.schedule or [], start=1):
            Schedule.objects.create(
                workshop=workshop,
                number=item.get("number", ""),
                label=item.get("label", ""),
                title=item.get("title", ""),
                text=item.get("text", ""),
                sort_order=idx,
            )

        for idx, item in enumerate(workshop.faqs or [], start=1):
            FAQ.objects.create(
                workshop=workshop,
                question=item.get("question", ""),
                answer=item.get("answer", ""),
                sort_order=idx,
            )


def reverse_relations_to_json(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")

    for workshop in Workshop.objects.all():
        workshop.intro_paragraphs = [item.text for item in workshop.intro_paragraph_items.all()]
        workshop.outcomes = [
            {"number": item.number, "title": item.title, "text": item.text}
            for item in workshop.outcome_items.all()
        ]
        workshop.audiences = [
            {"icon": item.icon, "label": item.label, "text": item.text}
            for item in workshop.audience_items.all()
        ]

        sessions = []
        current_key = None
        current_session = None
        for item in workshop.curriculum_items.all():
            if item.session_key != current_key:
                current_key = item.session_key
                current_session = {
                    "label": item.session_label,
                    "title": item.session_title,
                    "day": item.session_day,
                    "time": item.session_time,
                    "modules": [],
                }
                sessions.append(current_session)
            current_session["modules"].append(
                {"number": item.number, "title": item.title, "text": item.text}
            )
        workshop.curriculum = sessions

        workshop.benefits = [
            {
                "number": item.number,
                "kicker": item.kicker,
                "title": item.title,
                "text": item.text,
                "visual": item.visual,
            }
            for item in workshop.benefit_items.all()
        ]
        workshop.schedule = [
            {"number": item.number, "label": item.label, "title": item.title, "text": item.text}
            for item in workshop.schedule_items.all()
        ]
        workshop.faqs = [
            {"question": item.question, "answer": item.answer}
            for item in workshop.faq_items.all()
        ]
        workshop.save(
            update_fields=[
                "intro_paragraphs",
                "outcomes",
                "audiences",
                "curriculum",
                "benefits",
                "schedule",
                "faqs",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [("workshop", "0002_seed_workshops")]

    operations = [
        migrations.AddField(
            model_name="workshop",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Matikan saat masih menyiapkan draft. Workshop draft tidak muncul di website publik.",
            ),
        ),
        migrations.CreateModel(
            name="WorkshopIntroParagraph",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="intro_paragraph_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="WorkshopOutcome",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(blank=True, max_length=12)),
                ("title", models.CharField(max_length=160)),
                ("text", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="outcome_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="WorkshopAudience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("icon", models.CharField(blank=True, max_length=12)),
                ("label", models.CharField(max_length=160)),
                ("text", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="audience_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="WorkshopCurriculumModule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.SlugField(help_text="Gunakan nilai yang sama untuk modul dalam sesi yang sama, contoh: day-01 atau session-01.", max_length=80)),
                ("session_label", models.CharField(max_length=80)),
                ("session_title", models.CharField(max_length=220)),
                ("session_day", models.CharField(blank=True, max_length=80)),
                ("session_time", models.CharField(blank=True, max_length=80)),
                ("number", models.CharField(blank=True, max_length=12)),
                ("title", models.CharField(max_length=180)),
                ("text", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="curriculum_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="WorkshopBenefit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(blank=True, max_length=12)),
                ("kicker", models.CharField(blank=True, max_length=80)),
                ("title", models.CharField(max_length=180)),
                ("text", models.TextField()),
                ("visual", models.CharField(choices=[("live", "Live / 2 Hari"), ("practice", "Hands-on / Interface"), ("material", "Materi / Document"), ("flow", "Workflow"), ("replay", "Recording"), ("modules", "12+ Modul")], default="material", max_length=24)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="benefit_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="WorkshopScheduleItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(blank=True, max_length=12)),
                ("label", models.CharField(max_length=180)),
                ("title", models.CharField(max_length=180)),
                ("text", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="schedule_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="WorkshopFAQ",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=240)),
                ("answer", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("workshop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="faq_items", to="workshop.workshop")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.RunPython(migrate_json_to_relations, reverse_relations_to_json),
        migrations.RemoveField(model_name="workshop", name="intro_paragraphs"),
        migrations.RemoveField(model_name="workshop", name="outcomes"),
        migrations.RemoveField(model_name="workshop", name="audiences"),
        migrations.RemoveField(model_name="workshop", name="curriculum"),
        migrations.RemoveField(model_name="workshop", name="benefits"),
        migrations.RemoveField(model_name="workshop", name="schedule"),
        migrations.RemoveField(model_name="workshop", name="faqs"),
        migrations.AlterField(
            model_name="workshop",
            name="layout_variant",
            field=models.CharField(
                choices=[("research", "Latest / Research (Claude-style)"), ("productivity", "Productivity (ChatGPT-style)")],
                default="research",
                help_text="Untuk workshop baru, gunakan 'Latest / Research' agar memakai tampilan terbaru seperti halaman Claude untuk Riset.",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="workshop",
            name="is_archived",
            field=models.BooleanField(
                default=False,
                help_text="Opsional. Workshop yang tanggal akhirnya sudah lewat otomatis diperlakukan sebagai workshop sebelumnya.",
            ),
        ),
        migrations.AlterField(
            model_name="workshop",
            name="hero_image",
            field=models.CharField(blank=True, help_text="Path file di static, contoh: workshop/img/hero.jpg", max_length=255),
        ),
    ]
