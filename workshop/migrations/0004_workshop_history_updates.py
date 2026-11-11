from datetime import date

from django.db import migrations


def update_workshop_history(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Mentor = apps.get_model("workshop", "Mentor")
    WorkshopIntroParagraph = apps.get_model("workshop", "WorkshopIntroParagraph")
    WorkshopOutcome = apps.get_model("workshop", "WorkshopOutcome")
    WorkshopAudience = apps.get_model("workshop", "WorkshopAudience")
    WorkshopCurriculumModule = apps.get_model("workshop", "WorkshopCurriculumModule")
    WorkshopBenefit = apps.get_model("workshop", "WorkshopBenefit")
    WorkshopScheduleItem = apps.get_model("workshop", "WorkshopScheduleItem")
    WorkshopFAQ = apps.get_model("workshop", "WorkshopFAQ")

    # Seluruh workshop menggunakan harga yang sama.
    Workshop.objects.all().update(price_label="Rp390.000")

    # Koreksi tanggal workshop ChatGPT yang sudah selesai.
    Workshop.objects.filter(slug="chatgpt-pendataan-harian").update(
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 2),
        dates_label="1 & 2 Oktober 2026",
        days_label="Kamis & Jumat",
        price_label="Rp390.000",
        registration_note="Workshop ini telah selesai dilaksanakan pada 1 & 2 Oktober 2026.",
        is_archived=True,
        show_registration=False,
    )

    mentor = Mentor.objects.filter(name="Muhammad Angga Muttaqien").first() or Mentor.objects.first()
    if mentor is None:
        return

    workshop, _ = Workshop.objects.update_or_create(
        slug="gemini-laporan-kerja",
        defaults={
            "title": "Pakai Gemini untuk Membuat Laporan Kerja",
            "headline": "Pakai Gemini",
            "headline_accent": "untuk Membuat Laporan Kerja",
            "subtitle": "Workshop praktis untuk menyusun laporan kerja yang lebih cepat, rapi, dan konsisten.",
            "description": (
                "Belajar menggunakan Gemini untuk mengolah catatan kerja, merangkum informasi, "
                "menemukan poin penting, dan menyusunnya menjadi laporan yang lebih terstruktur."
            ),
            "meta_description": (
                "Workshop Pakai Gemini untuk Membuat Laporan Kerja oleh Indonesia AI, "
                "dilaksanakan pada 17 dan 18 September 2026."
            ),
            "layout_variant": "productivity",
            "eyebrow": "AI WORKSHOP • PRODUCTIVITY",
            "audience_label": (
                "Untuk profesional, admin, operasional, UMKM, dan siapa pun yang rutin membuat laporan kerja."
            ),
            "start_date": date(2026, 9, 17),
            "end_date": date(2026, 9, 18),
            "dates_label": "17 & 18 September 2026",
            "days_label": "Kamis & Jumat",
            "time_label": "19.30–21.00 WIB",
            "format_label": "Online",
            "duration_label": "2 Sesi • Total 3 Jam",
            "price_label": "Rp390.000",
            "registration_url": "",
            "show_registration": False,
            "is_archived": True,
            "is_published": True,
            "hero_image": "",
            "hero_badge": "GEMINI + WORK REPORT",
            "hero_flow": "Catatan → Analisis → Laporan",
            "hero_note": "Tidak perlu kemampuan programming",
            "intro_title": "Membuat laporan rutin tidak harus dimulai dari dokumen kosong setiap kali.",
            "audience_title": "Cocok untuk pekerjaan yang rutin mengubah informasi menjadi laporan.",
            "audience_intro": "Gunakan Gemini untuk membantu mengubah catatan kerja menjadi laporan yang lebih terstruktur.",
            "curriculum_title": "Dua sesi untuk membangun workflow laporan kerja dengan Gemini.",
            "curriculum_intro": (
                "Fokus workshop adalah membangun proses yang bisa digunakan kembali, "
                "mulai dari menyiapkan konteks hingga menghasilkan laporan yang siap ditinjau."
            ),
            "benefits_title": "Apa yang didapatkan dari workshop ini?",
            "benefits_intro": "Materi dan workflow praktis yang dapat diterapkan kembali setelah workshop selesai.",
            "schedule_title": "Dua sesi untuk mengubah catatan menjadi laporan yang lebih siap pakai.",
            "mentor": mentor,
            "mentor_section_title": "Belajar langsung bersama praktisi yang menggunakan AI dalam pekerjaan nyata.",
            "mentor_section_intro": (
                "Pendekatan workshop menekankan penggunaan AI yang praktis, terukur, "
                "dan mudah diadaptasi ke workflow masing-masing peserta."
            ),
            "registration_note": "Workshop ini telah selesai dilaksanakan pada 17 & 18 September 2026.",
        },
    )

    # Pastikan migration aman jika dijalankan ulang pada database pengembangan.
    WorkshopIntroParagraph.objects.filter(workshop=workshop).delete()
    WorkshopOutcome.objects.filter(workshop=workshop).delete()
    WorkshopAudience.objects.filter(workshop=workshop).delete()
    WorkshopCurriculumModule.objects.filter(workshop=workshop).delete()
    WorkshopBenefit.objects.filter(workshop=workshop).delete()
    WorkshopScheduleItem.objects.filter(workshop=workshop).delete()
    WorkshopFAQ.objects.filter(workshop=workshop).delete()

    intro_paragraphs = [
        "Catatan aktivitas, update tim, hasil diskusi, dan data operasional sering tersebar di banyak format sebelum akhirnya dibuat menjadi laporan.",
        "Di workshop ini, Gemini digunakan sebagai alat bantu untuk merangkum informasi, menemukan poin penting, dan menyusun draft laporan yang lebih konsisten untuk kemudian ditinjau manusia.",
    ]
    for idx, text in enumerate(intro_paragraphs, start=1):
        WorkshopIntroParagraph.objects.create(workshop=workshop, text=text, sort_order=idx)

    outcomes = [
        ("01", "Rapikan Catatan", "Mengubah catatan kerja yang tidak seragam menjadi input yang lebih terstruktur."),
        ("02", "Buat Ringkasan", "Merangkum informasi penting tanpa kehilangan konteks utama."),
        ("03", "Temukan Insight", "Membantu mengidentifikasi pola, isu, dan poin tindak lanjut dari data kerja."),
        ("04", "Susun Laporan", "Mengembangkan hasil analisis menjadi draft laporan yang lebih konsisten."),
    ]
    for idx, (number, title, text) in enumerate(outcomes, start=1):
        WorkshopOutcome.objects.create(
            workshop=workshop,
            number=number,
            title=title,
            text=text,
            sort_order=idx,
        )

    audiences = [
        ("A", "Admin & Operasional", "Untuk pekerjaan yang rutin merekap aktivitas, data, dan update harian."),
        ("T", "Team Lead", "Untuk membantu menyusun ringkasan progres, isu, dan tindak lanjut tim."),
        ("U", "UMKM", "Untuk membuat laporan sederhana dari catatan penjualan, pelanggan, atau operasional."),
        ("P", "Profesional", "Untuk siapa pun yang sering mengubah catatan dan informasi menjadi laporan kerja."),
    ]
    for idx, (icon, label, text) in enumerate(audiences, start=1):
        WorkshopAudience.objects.create(
            workshop=workshop,
            icon=icon,
            label=label,
            text=text,
            sort_order=idx,
        )

    modules = [
        ("day-01", "DAY 01", "Mengolah Catatan & Informasi Kerja", "Kamis", "19.30–21.00 WIB", "01", "Menyiapkan Data & Konteks", "Menentukan input, konteks, dan format keluaran agar Gemini memahami kebutuhan laporan."),
        ("day-01", "DAY 01", "Mengolah Catatan & Informasi Kerja", "Kamis", "19.30–21.00 WIB", "02", "Meringkas Catatan Kerja", "Mengubah catatan panjang menjadi ringkasan yang lebih singkat tanpa menghilangkan poin utama."),
        ("day-01", "DAY 01", "Mengolah Catatan & Informasi Kerja", "Kamis", "19.30–21.00 WIB", "03", "Ekstraksi Data & Insight", "Mengambil angka, kejadian, isu, dan tindak lanjut penting dari informasi yang tersedia."),
        ("day-02", "DAY 02", "Menyusun & Memperbaiki Laporan", "Jumat", "19.30–21.00 WIB", "04", "Membangun Struktur Laporan", "Menyusun bagian laporan agar konsisten dan mudah dipahami pembaca."),
        ("day-02", "DAY 02", "Menyusun & Memperbaiki Laporan", "Jumat", "19.30–21.00 WIB", "05", "Draft & Revisi dengan Gemini", "Mengembangkan draft, memperjelas kalimat, dan meminta critique sebelum laporan digunakan."),
        ("day-02", "DAY 02", "Menyusun & Memperbaiki Laporan", "Jumat", "19.30–21.00 WIB", "06", "Workflow Laporan Berkala", "Menggabungkan langkah-langkah workshop menjadi workflow yang bisa dipakai kembali."),
    ]
    for idx, item in enumerate(modules, start=1):
        (
            session_key,
            session_label,
            session_title,
            session_day,
            session_time,
            number,
            title,
            text,
        ) = item
        WorkshopCurriculumModule.objects.create(
            workshop=workshop,
            session_key=session_key,
            session_label=session_label,
            session_title=session_title,
            session_day=session_day,
            session_time=session_time,
            number=number,
            title=title,
            text=text,
            sort_order=idx,
        )

    benefits = [
        ("01", "LIVE LEARNING", "Live Workshop 2 Hari", "Belajar langsung dalam dua sesi interaktif bersama mentor.", "live"),
        ("02", "PRACTICE", "Hands-on Practice", "Langsung mencoba workflow Gemini menggunakan contoh kasus laporan kerja.", "practice"),
        ("03", "MATERIAL", "Materi Workshop", "Materi dapat digunakan kembali sebagai referensi setelah kelas.", "material"),
        ("04", "TEMPLATE", "Workflow Template", "Template alur kerja dari catatan menuju laporan yang siap ditinjau.", "flow"),
        ("05", "REPLAY", "Rekaman Kelas", "Pelajari kembali pembahasan workshop setelah sesi selesai.", "replay"),
        ("06", "BONUS LEARNING", "Belasan Modul Tools AI", "Materi tambahan untuk mengenal berbagai tools AI produktivitas.", "modules"),
    ]
    for idx, (number, kicker, title, text, visual) in enumerate(benefits, start=1):
        WorkshopBenefit.objects.create(
            workshop=workshop,
            number=number,
            kicker=kicker,
            title=title,
            text=text,
            visual=visual,
            sort_order=idx,
        )

    schedules = [
        ("01", "KAMIS • 19.30–21.00 WIB", "Mengolah Catatan & Informasi Kerja", "Menyiapkan konteks, meringkas catatan, dan mengekstraksi informasi penting."),
        ("02", "JUMAT • 19.30–21.00 WIB", "Menyusun & Memperbaiki Laporan", "Membangun struktur laporan, menghasilkan draft, dan membuat workflow yang dapat digunakan kembali."),
    ]
    for idx, (number, label, title, text) in enumerate(schedules, start=1):
        WorkshopScheduleItem.objects.create(
            workshop=workshop,
            number=number,
            label=label,
            title=title,
            text=text,
            sort_order=idx,
        )

    faqs = [
        ("Apakah workshop ini membutuhkan kemampuan coding?", "Tidak. Seluruh praktik menggunakan Gemini tanpa programming."),
        ("Apakah harus membawa data kerja sendiri?", "Tidak. Workshop menyediakan contoh yang dapat diikuti seluruh peserta."),
        ("Apakah Gemini akan menulis laporan sepenuhnya?", "Gemini digunakan untuk membantu merangkum, menyusun draft, dan melakukan revisi. Peninjauan serta keputusan akhir tetap dilakukan oleh pengguna."),
        ("Apakah peserta mendapatkan rekaman?", "Ya. Rekaman workshop dapat dipelajari kembali setelah sesi selesai."),
    ]
    for idx, (question, answer) in enumerate(faqs, start=1):
        WorkshopFAQ.objects.create(
            workshop=workshop,
            question=question,
            answer=answer,
            sort_order=idx,
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0003_admin_friendly_content"),
    ]

    operations = [
        migrations.RunPython(update_workshop_history, noop_reverse),
    ]
