from django.db import migrations


MENTOR_NAME = "Muhammad Angga Muttaqien, M.Eng."
LEGACY_NAME = "Muhammad Angga Muttaqien"

FULL_BIO = (
    "Kak Angga memiliki pengalaman lebih dari 10 tahun di bidang teknologi AI. "
    "Sebelumnya, ia berkarier sebagai AI Research Engineer di GRID Co., Ltd., "
    "dan saat ini aktif sebagai Research Assistant di National Institute of "
    "Advanced Industrial Science and Technology (AIST, 産業技術総合研究所), "
    "lembaga riset pemerintah Jepang yang berlokasi di Tokyo. "
    "Fokus dan minat risetnya saat ini meliputi Artificial Intelligence, "
    "Embodied AI, dan Human-Robot Interaction."
)


def consolidate_mentor_records(apps, schema_editor):
    Mentor = apps.get_model("workshop", "Mentor")
    Workshop = apps.get_model("workshop", "Workshop")

    # Scope the cleanup to the known duplicated mentor only. Other mentors
    # belong to independent workshop content and must not be deleted.
    mentors = list(
        Mentor.objects.filter(name__in=[MENTOR_NAME, LEGACY_NAME]).order_by("-pk")
    )
    if not mentors:
        return

    # Prefer a record that already has a complete biography. If more than
    # one record has it (migration 0012 populated both), prefer the newer ID.
    canonical = next((item for item in mentors if item.full_bio.strip()), mentors[0])

    # Repoint every existing workshop BEFORE removing duplicate records,
    # respecting the Workshop.mentor foreign key's PROTECT constraint.
    duplicate_ids = [item.pk for item in mentors if item.pk != canonical.pk]
    if duplicate_ids:
        Workshop.objects.filter(mentor_id__in=duplicate_ids).update(mentor_id=canonical.pk)
        Mentor.objects.filter(pk__in=duplicate_ids).delete()

    updates = []
    if canonical.name != MENTOR_NAME:
        canonical.name = MENTOR_NAME
        updates.append("name")
    if not canonical.full_bio.strip():
        canonical.full_bio = FULL_BIO
        updates.append("full_bio")
    if updates:
        canonical.save(update_fields=updates)


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0012_mentor_full_bio"),
    ]

    operations = [
        migrations.RunPython(consolidate_mentor_records, migrations.RunPython.noop),
    ]
