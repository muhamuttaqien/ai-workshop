from django.db import migrations


THIRD_LESSONS = [
    {
        "course": "chatgpt-untuk-aktivitas-sehari-hari",
        "slug": "memeriksa-hasil-chatgpt",
        "title": "Memeriksa Hasil ChatGPT",
        "content": (
            "Jawaban AI dapat terdengar meyakinkan meskipun mengandung kesalahan. "
            "Karena itu, langkah penting setelah memakai ChatGPT adalah memeriksa "
            "fakta, angka, nama, dan sumber yang relevan.\n\n"
            "Praktik: mintalah ChatGPT menyusun ringkasan sebuah topik yang sudah "
            "kamu pahami. Tandai tiga klaim penting, lalu bandingkan dengan sumber "
            "yang dapat dipercaya sebelum menggunakan hasilnya."
        ),
        "question": "Apa yang perlu diprioritaskan sebelum membagikan hasil ChatGPT?",
        "options": [
            "Menyalin tanpa membaca",
            "Memastikan panjang jawabannya",
            "Memeriksa fakta dan sumber penting",
            "Menghapus konteks",
        ],
        "correct": "c",
        "explanation": "Pemeriksaan fakta dan sumber penting membantu menghindari penyebaran informasi yang keliru.",
    },
    {
        "course": "claude-untuk-riset-dan-menulis",
        "slug": "memverifikasi-sumber-dan-kutipan",
        "title": "Memverifikasi Sumber dan Kutipan",
        "content": (
            "Ketika Claude membantu merangkum atau menyusun argumen, setiap rujukan "
            "tetap perlu dicocokkan dengan publikasi aslinya. Hindari menggunakan "
            "kutipan yang belum ditemukan pada sumber yang sah.\n\n"
            "Praktik: pilih satu paragraf ringkasan berbantuan AI, identifikasi "
            "klaim pentingnya, lalu cari bagian dokumen asli yang mendukung "
            "atau membantah klaim tersebut."
        ),
        "question": "Bagaimana menggunakan kutipan dari hasil AI secara bertanggung jawab?",
        "options": [
            "Memverifikasi kutipan pada sumber asli",
            "Menganggap referensi pasti ada",
            "Mengutip tanpa membaca dokumen",
            "Menghapus nama penulis",
        ],
        "correct": "a",
        "explanation": "Kutipan dan referensi harus dapat ditelusuri ke sumber aslinya.",
    },
    {
        "course": "canva-ai-untuk-konten-visual",
        "slug": "mengevaluasi-desain-konten",
        "title": "Mengevaluasi Desain Konten",
        "content": (
            "Desain visual yang baik bukan hanya menarik, tetapi juga mudah dibaca "
            "dan sesuai tujuan komunikasi. Periksa hierarki informasi, kontras, "
            "konsistensi warna merek, dan kejelasan ajakan bertindak.\n\n"
            "Praktik: buat satu desain edukasi singkat, kemudian periksa apakah "
            "pesan utama langsung terlihat pada layar ponsel."
        ),
        "question": "Apa tanda bahwa desain konten efektif?",
        "options": [
            "Semua elemen menggunakan warna berbeda",
            "Pesan utama jelas dan mudah dibaca",
            "Teks dibuat sekecil mungkin",
            "Efek dekorasi lebih penting daripada informasi",
        ],
        "correct": "b",
        "explanation": "Keterbacaan dan kejelasan pesan adalah dasar komunikasi visual yang efektif.",
    },
    {
        "course": "gemini-untuk-produktivitas-dan-laporan",
        "slug": "meninjau-laporan-dengan-ai",
        "title": "Meninjau Laporan dengan AI",
        "content": (
            "Gemini dapat membantu meninjau struktur laporan, mencari bagian yang "
            "kurang jelas, dan mengusulkan penyuntingan bahasa. Namun, data "
            "dan keputusan yang disajikan tetap perlu diperiksa manusia.\n\n"
            "Praktik: siapkan contoh laporan tanpa data sensitif. Mintalah AI "
            "mengidentifikasi bagian yang perlu diperjelas, lalu tinjau setiap "
            "usulannya sebelum memperbaiki laporan."
        ),
        "question": "Langkah tepat setelah AI mengusulkan revisi laporan adalah?",
        "options": [
            "Menerima seluruh revisi otomatis",
            "Membuang semua bukti pendukung",
            "Menghapus bagian kesimpulan",
            "Meninjau usulan dan memeriksa data aslinya",
        ],
        "correct": "d",
        "explanation": "Usulan AI perlu ditinjau serta dicocokkan dengan data dan tujuan laporan.",
    },
    {
        "course": "notebooklm-untuk-belajar-dari-dokumen",
        "slug": "menyusun-catatan-belajar",
        "title": "Menyusun Catatan Belajar",
        "content": (
            "Setelah mengeksplorasi sumber melalui NotebookLM, rangkum ide penting "
            "dengan bahasamu sendiri. Kelompokkan konsep utama, hal yang belum "
            "dipahami, dan pertanyaan untuk dipelajari berikutnya.\n\n"
            "Praktik: pilih satu dokumen yang kamu miliki, lalu susun catatan "
            "belajar berisi tiga gagasan utama dan dua pertanyaan lanjutan. "
            "Bandingkan kembali hasilnya dengan dokumen asli."
        ),
        "question": "Apa fungsi catatan belajar setelah menelaah dokumen?",
        "options": [
            "Menggantikan semua dokumen asli",
            "Menghilangkan pertanyaan yang belum terjawab",
            "Merangkum konsep dan mengidentifikasi hal yang perlu dipelajari",
            "Menyalin semua teks tanpa memilih ide",
        ],
        "correct": "c",
        "explanation": "Catatan belajar membantu mengorganisasi pemahaman dan menentukan pertanyaan lanjutan.",
    },
]


def add_third_lessons(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Lesson = apps.get_model("courses", "Lesson")
    QuizQuestion = apps.get_model("courses", "QuizQuestion")

    for item in THIRD_LESSONS:
        course = Course.objects.filter(slug=item["course"]).first()
        if course is None:
            continue
        lesson, _ = Lesson.objects.get_or_create(
            course=course, slug=item["slug"],
            defaults={
                "title": item["title"],
                "summary": "Materi pengantar, latihan praktis, dan kuis singkat.",
                "content": item["content"],
                "sort_order": 3,
                "is_published": True,
            },
        )
        if not QuizQuestion.objects.filter(lesson=lesson).exists():
            QuizQuestion.objects.create(
                lesson=lesson,
                question=item["question"],
                option_a=item["options"][0],
                option_b=item["options"][1],
                option_c=item["options"][2],
                option_d=item["options"][3],
                correct_option=item["correct"],
                explanation=item["explanation"],
            )


class Migration(migrations.Migration):
    dependencies = [("courses", "0005_seed_intro_lessons")]

    operations = [
        migrations.RunPython(add_third_lessons, migrations.RunPython.noop),
    ]
