from django.db import migrations


def add_courses(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    examples = [
        {
            "slug": "gemini-untuk-produktivitas-dan-laporan",
            "title": "Gemini untuk Produktivitas dan Laporan",
            "tool_label": "Gemini",
            "short_description": "Gunakan Gemini untuk merangkum informasi, mengatur pekerjaan, dan menyiapkan laporan yang lebih terstruktur.",
            "description": (
                "Pelajari cara menggunakan Gemini untuk membantu pekerjaan sehari-hari, "
                "mulai dari menyusun instruksi hingga merangkum informasi dan "
                "menyiapkan draf laporan. Latih juga cara memeriksa akurasi "
                "dan memperbaiki hasil keluaran AI."
            ),
            "audience": "Mahasiswa, staf administrasi, tim operasional, dan profesional.",
            "learning_objectives": (
                "Menyusun prompt yang jelas untuk Gemini\n"
                "Merangkum catatan dan informasi pekerjaan\n"
                "Menyiapkan draf laporan terstruktur\n"
                "Mengevaluasi dan menyunting hasil AI"
            ),
            "level": "beginner",
            "sort_order": 4,
        },
        {
            "slug": "notebooklm-untuk-belajar-dari-dokumen",
            "title": "NotebookLM untuk Belajar dari Dokumen",
            "tool_label": "NotebookLM",
            "short_description": "Belajar memahami dokumen, membuat ringkasan, dan mengeksplorasi pertanyaan dengan bantuan AI.",
            "description": (
                "Kursus pengantar penggunaan NotebookLM sebagai pendamping belajar "
                "berbasis dokumen. Pelajari cara menyiapkan sumber, membuat pertanyaan "
                "yang relevan, membandingkan informasi, dan memeriksa kembali "
                "jawaban terhadap dokumen asli."
            ),
            "audience": "Pelajar, mahasiswa, pengajar, peneliti, dan pembelajar mandiri.",
            "learning_objectives": (
                "Menyiapkan dokumen sebagai bahan pembelajaran\n"
                "Membuat ringkasan dan pertanyaan dari sumber\n"
                "Mengeksplorasi hubungan antar-informasi\n"
                "Memeriksa jawaban terhadap sumber aslinya"
            ),
            "level": "beginner",
            "sort_order": 5,
        },
    ]
    for item in examples:
        Course.objects.get_or_create(
            slug=item["slug"],
            defaults={
                **{key: value for key, value in item.items() if key != "slug"},
                "status": "coming_soon",
                "is_published": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_sample_courses"),
    ]

    operations = [
        migrations.RunPython(add_courses, migrations.RunPython.noop),
    ]
