from django.db import migrations


def create_example_courses(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    examples = [
        {
            "slug": "chatgpt-untuk-aktivitas-sehari-hari",
            "title": "ChatGPT untuk Aktivitas Sehari-hari",
            "tool_label": "ChatGPT",
            "short_description": "Memahami cara memanfaatkan ChatGPT untuk menulis, merangkum, dan menyelesaikan pekerjaan rutin.",
            "description": (
                "Kursus pengantar penggunaan ChatGPT untuk kebutuhan sehari-hari. "
                "Pelajari cara menyusun instruksi yang jelas, mengevaluasi jawaban, "
                "dan mengadaptasi AI menjadi pendamping pekerjaan dan pembelajaran."
            ),
            "audience": "Pemula, mahasiswa, profesional, dan siapa saja yang ingin memulai dengan AI.",
            "learning_objectives": (
                "Mengenali kemampuan dan batasan ChatGPT\n"
                "Menyusun instruksi yang lebih efektif\n"
                "Menggunakan AI untuk menulis dan merangkum\n"
                "Memeriksa hasil sebelum digunakan"
            ),
            "level": "beginner",
            "sort_order": 1,
        },
        {
            "slug": "claude-untuk-riset-dan-menulis",
            "title": "Claude untuk Riset dan Menulis",
            "tool_label": "Claude",
            "short_description": "Eksplorasi penggunaan Claude untuk memahami literatur, menyusun argumen, dan menyunting tulisan.",
            "description": (
                "Kursus pengantar pemanfaatan Claude untuk membaca dokumen, "
                "membandingkan gagasan, mengeksplorasi pertanyaan, dan menyusun "
                "tulisan lebih terarah dengan tetap memeriksa sumber asli."
            ),
            "audience": "Mahasiswa, peneliti, akademisi, dan profesional yang bekerja dengan dokumen.",
            "learning_objectives": (
                "Memahami fungsi AI sebagai pendamping riset\n"
                "Membaca dan membandingkan dokumen\n"
                "Mengembangkan kerangka tulisan\n"
                "Memeriksa klaim dan sumber informasi"
            ),
            "level": "beginner",
            "sort_order": 2,
        },
        {
            "slug": "canva-ai-untuk-konten-visual",
            "title": "Canva AI untuk Konten Visual",
            "tool_label": "Canva AI",
            "short_description": "Belajar mengembangkan ide dan visual untuk kebutuhan konten komunikasi sehari-hari.",
            "description": (
                "Kursus pengantar penggunaan Canva AI untuk membantu proses kreatif: "
                "dari ide konten dan penyusunan brief hingga visual yang konsisten "
                "dan dapat disesuaikan untuk berbagai kebutuhan."
            ),
            "audience": "Pembuat konten, tim marketing, UMKM, dan profesional non-desainer.",
            "learning_objectives": (
                "Menentukan tujuan dan audiens konten\n"
                "Mengembangkan ide kreatif dengan bantuan AI\n"
                "Membuat draft visual yang mudah disesuaikan\n"
                "Menjaga konsistensi pesan dan desain"
            ),
            "level": "beginner",
            "sort_order": 3,
        },
    ]
    for example in examples:
        Course.objects.get_or_create(
            slug=example["slug"],
            defaults={
                **{key: value for key, value in example.items() if key != "slug"},
                "status": "coming_soon",
                "is_published": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [("courses", "0001_initial")]

    operations = [
        migrations.RunPython(create_example_courses, migrations.RunPython.noop),
    ]
