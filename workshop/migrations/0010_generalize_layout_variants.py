from django.db import migrations, models


def rename_layout_variants(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    mapping = {
        "research": "editorial",
        "productivity": "workflow",
        "reporting": "dashboard",
    }
    for old_value, new_value in mapping.items():
        Workshop.objects.filter(layout_variant=old_value).update(layout_variant=new_value)


def restore_layout_variants(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    mapping = {
        "editorial": "research",
        "workflow": "productivity",
        "dashboard": "reporting",
        "showcase": "research",
        "guide": "research",
    }
    for new_value, old_value in mapping.items():
        Workshop.objects.filter(layout_variant=new_value).update(layout_variant=old_value)


class Migration(migrations.Migration):

    dependencies = [
        ("workshop", "0009_fix_chatgpt_schedule_and_research_hero"),
    ]

    operations = [
        migrations.RunPython(rename_layout_variants, restore_layout_variants),
        migrations.AlterField(
            model_name="workshop",
            name="layout_variant",
            field=models.CharField(
                choices=[
                    ("editorial", "Editorial — Narrative & Knowledge"),
                    ("workflow", "Workflow — Process & Hands-on"),
                    ("dashboard", "Dashboard — Data & Reporting"),
                    ("showcase", "Showcase — Visual & Creative"),
                    ("guide", "Guide — Step-by-step & Beginner"),
                ],
                default="editorial",
                help_text=(
                    "Pilih gaya halaman berdasarkan cara materi ingin dipresentasikan: "
                    "Editorial, Workflow, Dashboard, Showcase, atau Guide."
                ),
                max_length=32,
            ),
        ),
    ]
