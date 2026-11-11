from datetime import date

from django.db import migrations, models


MODULES_TEXT = (
    "Belasan modul tambahan tentang tools AI seperti ChatGPT, Claude, Gemini, "
    "Perplexity dan lainnya."
)


def update_workshops(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Mentor = apps.get_model("workshop", "Mentor")
    WorkshopIntroParagraph = apps.get_model("workshop", "WorkshopIntroParagraph")
    WorkshopOutcome = apps.get_model("workshop", "WorkshopOutcome")
    WorkshopAudience = apps.get_model("workshop", "WorkshopAudience")
    WorkshopCurriculumModule = apps.get_model("workshop", "WorkshopCurriculumModule")
    WorkshopBenefit = apps.get_model("workshop", "WorkshopBenefit")
    WorkshopScheduleItem = apps.get_model("workshop", "WorkshopScheduleItem")
    WorkshopFAQ = apps.get_model("workshop", "WorkshopFAQ")

    # Standardisasi seluruh workshop yang sudah ada.
    Workshop.objects.all().update(
        format_label="Zoom Online",
        price_label="Rp390.000",
    )
    WorkshopBenefit.objects.filter(visual="modules").update(text=MODULES_TEXT)

    mentor = Mentor.objects.filter(name="Muhammad Angga Muttaqien").first() or Mentor.objects.first()
    if mentor is None:
        return

    workshop, _ = Workshop.objects.update_or_create(
        slug="perplexity-riset-pasar-kompetitor",
        defaults={
            "title": "Pakai Perplexity untuk Riset Pasar & Kompetitor",
            "headline": "Pakai Perplexity",
            "headline_accent": "untuk Riset Pasar & Kompetitor",
            "subtitle": "Workshop praktis untuk mencari sumber, memetakan pasar, dan membandingkan kompetitor secara lebih terstruktur.",
            "description": (
                "Belajar menggunakan Perplexity untuk mempercepat riset pasar dan kompetitor: "
                "mulai dari merumuskan pertanyaan, mencari sumber, membandingkan pemain, hingga "
                "menyusun insight yang dapat ditinjau kembali."
            ),
            "meta_description": (
                "Workshop Pakai Perplexity untuk Riset Pasar & Kompetitor oleh Indonesia AI, "
                "dilaksanakan pada 3 dan 4 September 2026."
            ),
            "layout_variant": "research",
            "eyebrow": "AI WORKSHOP • MARKET RESEARCH",
            "audience_label": (
                "Untuk profesional, business owner, marketing, product, dan siapa pun yang perlu melakukan riset pasar secara rutin."
            ),
            "start_date": date(2026, 9, 3),
            "end_date": date(2026, 9, 4),
            "dates_label": "3 & 4 September 2026",
            "days_label": "Kamis & Jumat",
            "time_label": "19.30–21.00 WIB",
            "format_label": "Zoom Online",
            "duration_label": "2 Sesi • Total 3 Jam",
            "price_label": "Rp390.000",
            "registration_url": "",
            "show_registration": False,
            "is_archived": True,
            "is_published": True,
            "hero_image": "",
            "hero_badge": "PERPLEXITY + MARKET RESEARCH",
            "hero_flow": "Question → Sources → Compare → Insight",
            "hero_note": "Tidak perlu kemampuan programming",
            "intro_title": "Riset pasar yang baik bukan sekadar mengumpulkan banyak link.",
            "audience_title": "Cocok untuk pekerjaan yang membutuhkan informasi eksternal sebelum mengambil keputusan.",
            "audience_intro": (
                "Gunakan Perplexity untuk membangun proses pencarian dan perbandingan yang lebih sistematis, sambil tetap memeriksa sumber aslinya."
            ),
            "curriculum_title": "Dua sesi untuk membangun workflow riset pasar dengan Perplexity.",
            "curriculum_intro": (
                "Fokus workshop adalah membuat proses riset yang dapat diulang: dari pertanyaan awal, "
                "pencarian sumber, pemetaan kompetitor, hingga sintesis insight."
            ),
            "benefits_title": "Apa yang akan kamu dapatkan?",
            "benefits_intro": "Materi, praktik, dan template yang dapat digunakan kembali untuk berbagai kebutuhan riset pasar.",
            "schedule_title": "Dua sesi dari pencarian sumber hingga insight yang siap ditinjau.",
            "mentor": mentor,
            "mentor_section_title": "Belajar langsung bersama praktisi yang menggunakan AI untuk riset dan pekerjaan nyata.",
            "mentor_section_intro": (
                "Pendekatan workshop menekankan cara menggunakan AI sebagai alat bantu riset, "
                "bukan pengganti evaluasi manusia terhadap sumber dan kesimpulan."
            ),
            "registration_note": "Workshop ini telah selesai dilaksanakan pada 3 & 4 September 2026.",
        },
    )

    # Bersihkan hanya konten anak workshop seed ini agar migration deterministik.
    WorkshopIntroParagraph.objects.filter(workshop=workshop).delete()
    WorkshopOutcome.objects.filter(workshop=workshop).delete()
    WorkshopAudience.objects.filter(workshop=workshop).delete()
    WorkshopCurriculumModule.objects.filter(workshop=workshop).delete()
    WorkshopBenefit.objects.filter(workshop=workshop).delete()
    WorkshopScheduleItem.objects.filter(workshop=workshop).delete()
    WorkshopFAQ.objects.filter(workshop=workshop).delete()

    intros = [
        (
            "Riset pasar sering dimulai dari pencarian yang terlalu luas, tab browser yang menumpuk, "
            "dan catatan yang sulit dibandingkan satu sama lain."
        ),
        (
            "Di workshop ini, Perplexity digunakan untuk membantu merumuskan pencarian, menemukan sumber, "
            "membandingkan pemain, dan menyusun insight awal yang kemudian tetap diverifikasi oleh peserta."
        ),
    ]
    for idx, text in enumerate(intros, start=1):
        WorkshopIntroParagraph.objects.create(workshop=workshop, text=text, sort_order=idx)

    outcomes = [
        ("01", "Tentukan Pertanyaan", "Mengubah kebutuhan bisnis menjadi pertanyaan riset yang lebih fokus."),
        ("02", "Temukan Sumber", "Mencari informasi dan sumber yang relevan untuk pasar yang sedang dipelajari."),
        ("03", "Bandingkan Kompetitor", "Menyusun perbandingan pemain, positioning, penawaran, dan informasi penting lainnya."),
        ("04", "Tarik Insight", "Menyintesis hasil riset menjadi poin yang lebih mudah digunakan untuk diskusi dan keputusan."),
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
        ("B", "Business Owner", "Untuk memahami pasar, pemain, dan perubahan yang relevan dengan bisnis."),
        ("M", "Marketing", "Untuk riset audiens, kategori, kompetitor, dan bahan penyusunan strategi."),
        ("P", "Product Team", "Untuk landscape research, benchmarking, dan eksplorasi kebutuhan pengguna."),
        ("C", "Consultant & Professional", "Untuk mempercepat desk research sebelum analisis yang lebih mendalam."),
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
        (
            "day-01", "DAY 01", "Mencari & Memetakan Informasi", "Kamis", "19.30–21.00 WIB",
            "01", "Merumuskan Research Question", "Membuat pertanyaan yang cukup spesifik agar proses pencarian menghasilkan informasi yang relevan."
        ),
        (
            "day-01", "DAY 01", "Mencari & Memetakan Informasi", "Kamis", "19.30–21.00 WIB",
            "02", "Pencarian Berbasis Sumber", "Menggunakan Perplexity untuk menemukan informasi sambil tetap melacak sumber yang mendasarinya."
        ),
        (
            "day-01", "DAY 01", "Mencari & Memetakan Informasi", "Kamis", "19.30–21.00 WIB",
            "03", "Membangun Market Landscape", "Mengelompokkan pemain, kategori, tren, dan informasi awal menjadi peta yang lebih terstruktur."
        ),
        (
            "day-02", "DAY 02", "Membandingkan & Menyusun Insight", "Jumat", "19.30–21.00 WIB",
            "04", "Competitive Comparison", "Membangun kerangka perbandingan agar kompetitor tidak dinilai dari informasi yang terpisah-pisah."
        ),
        (
            "day-02", "DAY 02", "Membandingkan & Menyusun Insight", "Jumat", "19.30–21.00 WIB",
            "05", "Validasi & Cross-check", "Memeriksa kembali klaim penting ke sumber asli dan membedakan fakta dari interpretasi."
        ),
        (
            "day-02", "DAY 02", "Membandingkan & Menyusun Insight", "Jumat", "19.30–21.00 WIB",
            "06", "Research Brief", "Mengubah hasil pencarian dan perbandingan menjadi ringkasan riset yang lebih siap dibahas."
        ),
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
        ("02", "PRACTICE", "Hands-on Practice", "Langsung mencoba workflow Perplexity menggunakan contoh kasus riset pasar.", "practice"),
        ("03", "MATERIAL", "Materi Workshop", "Materi dapat digunakan kembali sebagai referensi setelah kelas.", "material"),
        ("04", "TEMPLATE", "Research Workflow Template", "Template dari research question menuju source map, comparison, dan insight.", "flow"),
        ("05", "REPLAY", "Rekaman Kelas", "Pelajari kembali pembahasan workshop setelah sesi selesai.", "replay"),
        ("06", "BONUS LEARNING", "Belasan Modul Tools AI", MODULES_TEXT, "modules"),
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

    schedule = [
        (
            "01", "KAMIS • 19.30–21.00 WIB", "Mencari & Memetakan Informasi",
            "Research question, pencarian berbasis sumber, dan market landscape."
        ),
        (
            "02", "JUMAT • 19.30–21.00 WIB", "Membandingkan & Menyusun Insight",
            "Competitive comparison, validasi sumber, dan research brief."
        ),
    ]
    for idx, (number, label, title, text) in enumerate(schedule, start=1):
        WorkshopScheduleItem.objects.create(
            workshop=workshop,
            number=number,
            label=label,
            title=title,
            text=text,
            sort_order=idx,
        )

    faqs = [
        ("Apakah workshop ini cocok untuk pemula?", "Ya. Workshop berfokus pada workflow praktis dan tidak membutuhkan kemampuan programming."),
        ("Apakah harus memiliki bisnis sendiri?", "Tidak. Contoh dapat diterapkan untuk pekerjaan marketing, product, consulting, maupun kebutuhan riset profesional lainnya."),
        ("Apakah Perplexity menggantikan proses verifikasi sumber?", "Tidak. Peserta tetap diarahkan untuk membuka dan menilai sumber asli sebelum menggunakan informasi penting."),
        ("Apakah mendapatkan rekaman?", "Ya. Peserta mendapatkan rekaman kelas untuk dipelajari kembali."),
        ("Apakah mendapatkan materi tambahan?", MODULES_TEXT),
    ]
    for idx, (question, answer) in enumerate(faqs, start=1):
        WorkshopFAQ.objects.create(
            workshop=workshop,
            question=question,
            answer=answer,
            sort_order=idx,
        )


def reverse_seed(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Workshop.objects.filter(slug="perplexity-riset-pasar-kompetitor").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0005_reporting_layout_variant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workshop",
            name="format_label",
            field=models.CharField(default="Zoom Online", max_length=80),
        ),
        migrations.RunPython(update_workshops, reverse_seed),
    ]
