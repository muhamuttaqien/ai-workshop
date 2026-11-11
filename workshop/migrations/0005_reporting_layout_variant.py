from django.db import migrations, models


def set_gemini_reporting_layout(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Workshop.objects.filter(slug="gemini-laporan-kerja").update(layout_variant="reporting")


def restore_gemini_productivity_layout(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Workshop.objects.filter(slug="gemini-laporan-kerja").update(layout_variant="productivity")


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0004_workshop_history_updates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workshop",
            name="layout_variant",
            field=models.CharField(
                choices=[
                    ("research", "Latest / Research (Claude-style)"),
                    ("productivity", "Productivity (ChatGPT-style)"),
                    ("reporting", "Reporting (Gemini-style)"),
                ],
                default="research",
                help_text=(
                    "Untuk workshop baru, gunakan 'Latest / Research' agar memakai tampilan "
                    "terbaru seperti halaman Claude untuk Riset."
                ),
                max_length=32,
            ),
        ),
        migrations.RunPython(set_gemini_reporting_layout, restore_gemini_productivity_layout),
    ]
