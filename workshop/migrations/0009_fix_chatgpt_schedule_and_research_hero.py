from datetime import date

from django.db import migrations


def fix_chatgpt_schedule(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    WorkshopCurriculumModule = apps.get_model("workshop", "WorkshopCurriculumModule")
    WorkshopScheduleItem = apps.get_model("workshop", "WorkshopScheduleItem")

    workshop = Workshop.objects.filter(slug="chatgpt-pendataan-harian").first()
    if workshop is None:
        return

    # Pastikan seluruh metadata utama konsisten dengan tanggal aktual.
    Workshop.objects.filter(pk=workshop.pk).update(
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 2),
        dates_label="1 & 2 Oktober 2026",
        days_label="Kamis & Jumat",
        meta_description=(
            "Workshop Pakai ChatGPT untuk Pendataan Harian oleh Indonesia AI, "
            "dilaksanakan 1 dan 2 Oktober 2026."
        ),
        registration_note="Workshop ini telah selesai dilaksanakan pada 1 & 2 Oktober 2026.",
    )

    # Koreksi semua modul pada sesi kedua, bukan hanya tanggal utama workshop.
    WorkshopCurriculumModule.objects.filter(
        workshop=workshop,
        session_key="session-02",
    ).update(
        session_day="Jumat",
        session_time="19.30–21.00 WIB",
    )

    # Koreksi kartu jadwal yang tampil di halaman.
    WorkshopScheduleItem.objects.filter(
        workshop=workshop,
        sort_order=1,
    ).update(
        label="KAMIS • 1 OKTOBER • 19.30–21.00 WIB",
    )

    WorkshopScheduleItem.objects.filter(
        workshop=workshop,
        sort_order=2,
    ).update(
        label="JUMAT • 2 OKTOBER • 19.30–21.00 WIB",
    )


def reverse_fix(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    WorkshopCurriculumModule = apps.get_model("workshop", "WorkshopCurriculumModule")
    WorkshopScheduleItem = apps.get_model("workshop", "WorkshopScheduleItem")

    workshop = Workshop.objects.filter(slug="chatgpt-pendataan-harian").first()
    if workshop is None:
        return

    Workshop.objects.filter(pk=workshop.pk).update(
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 3),
        dates_label="1 & 3 Oktober 2026",
        days_label="Kamis & Sabtu",
        meta_description=(
            "Workshop Pakai ChatGPT untuk Pendataan Harian oleh Indonesia AI, "
            "dilaksanakan 1 dan 3 Oktober 2026."
        ),
        registration_note="Workshop ini telah selesai dilaksanakan pada 1 & 3 Oktober 2026.",
    )

    WorkshopCurriculumModule.objects.filter(
        workshop=workshop,
        session_key="session-02",
    ).update(session_day="Sabtu")

    WorkshopScheduleItem.objects.filter(
        workshop=workshop,
        sort_order=2,
    ).update(label="SABTU • 3 OKTOBER • 19.30–21.00 WIB")


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0008_alter_mentor_photo"),
    ]

    operations = [
        migrations.RunPython(fix_chatgpt_schedule, reverse_fix),
    ]
