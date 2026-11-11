from django.db import migrations


# Introductory text and quizzes are available as editable examples.
# No video URLs are invented; upload/paste real YouTube video IDs in Admin.
EXAMPLES = [
    (
        "chatgpt-untuk-aktivitas-sehari-hari",
        [
            ("mengenal-chatgpt", "Mengenal ChatGPT",
             "ChatGPT adalah asisten AI berbasis percakapan yang dapat membantu menyusun teks, merangkum informasi, dan mengeksplorasi ide. Hasilnya tetap perlu diperiksa, terutama jika menyangkut fakta atau keputusan penting.\n\nMulailah dengan menyebutkan tujuan, konteks, dan bentuk jawaban yang kamu inginkan. Misalnya, minta ChatGPT merangkum catatan dalam lima poin penting.",
             "Apa yang perlu dilakukan sebelum menggunakan informasi dari ChatGPT?",
             ["Langsung menyebarkannya", "Memeriksa kembali informasi penting", "Menghapus konteks pertanyaan", "Selalu menyalin hasil apa adanya"], "b",
             "ChatGPT dapat menghasilkan kekeliruan, sehingga informasi penting tetap perlu diverifikasi."),
            ("menulis-prompt-yang-jelas", "Menulis Prompt yang Jelas",
             "Prompt yang baik menjelaskan apa yang ingin dicapai, konteks pengguna, dan format keluaran. Instruksi yang spesifik biasanya membantu menghasilkan respons yang lebih sesuai.\n\nCoba bandingkan 'Buatkan email' dengan 'Buatkan email profesional untuk meminta jadwal rapat, maksimal 100 kata, menggunakan bahasa Indonesia yang sopan'.",
             "Prompt mana yang paling jelas?",
             ["Buat sesuatu", "Bantu saya", "Tulis email rapat maksimal 100 kata dengan nada sopan", "Terserah kamu"], "c",
             "Tujuan, batasan, dan format membantu memperjelas instruksi."),
        ],
    ),
    (
        "claude-untuk-riset-dan-menulis",
        [
            ("mengenal-claude", "Mengenal Claude",
             "Claude adalah asisten AI yang dapat membantu mengeksplorasi ide, membaca teks, dan memperbaiki struktur tulisan. Gunakan AI sebagai pendamping berpikir, bukan sebagai pengganti pemeriksaan sumber.\n\nSaat menganalisis dokumen, mulailah dengan menjelaskan pertanyaan riset dan jenis jawaban yang diharapkan.",
             "Apa praktik terbaik ketika AI merangkum dokumen?",
             ["Memastikan ringkasan sesuai sumber", "Menganggap semua klaim benar", "Menghilangkan sumber asli", "Tidak membaca ringkasan"], "a",
             "Ringkasan AI perlu dibandingkan dengan dokumen aslinya."),
            ("merancang-kerangka-tulisan", "Merancang Kerangka Tulisan",
             "Kerangka membantu menempatkan ide dalam urutan yang mudah dipahami. Claude dapat membantu mengusulkan bagian pendahuluan, pembahasan, dan kesimpulan.\n\nMintalah beberapa alternatif kerangka, pilih yang paling cocok, kemudian tulis dan periksa kembali argumen serta referensinya.",
             "Peran AI yang tepat dalam menulis karya akademik adalah?",
             ["Mengarang kutipan ilmiah", "Menggantikan pemeriksaan referensi", "Menentukan kesimpulan tanpa bukti", "Membantu merancang kerangka yang kemudian ditinjau"], "d",
             "AI dapat membantu menyusun ide, tetapi validasi isi tetap tanggung jawab penulis."),
        ],
    ),
    (
        "canva-ai-untuk-konten-visual",
        [
            ("mengenal-canva-ai", "Mengenal Canva AI",
             "Canva menyediakan fitur berbantuan AI untuk mendukung proses kreatif, seperti pengembangan ide dan penyusunan materi visual. Awali pekerjaan dengan menentukan sasaran konten.\n\nTentukan audiens, kanal publikasi, dan pesan utama sebelum membuat desain agar hasil visual lebih relevan.",
             "Apa yang sebaiknya ditentukan sebelum membuat visual?",
             ["Hanya ukuran font", "Audiens dan tujuan pesan", "Jumlah efek animasi", "Warna acak"], "b",
             "Audiens dan tujuan menjadi dasar keputusan desain yang konsisten."),
            ("membuat-brief-konten", "Membuat Brief Konten",
             "Brief konten menyatukan tujuan, gaya visual, pesan, dan kebutuhan format. Dengan brief yang jelas, ide berbantuan AI lebih mudah dievaluasi.\n\nCoba tulis brief singkat untuk sebuah unggahan edukasi: sasaran pembaca, satu pesan utama, warna merek, dan ajakan bertindak.",
             "Brief yang berguna memuat apa?",
             ["Tujuan, audiens, dan pesan", "Hanya gambar latar", "Hanya nama file", "Tanpa konteks"], "a",
             "Brief membantu AI dan pembuat konten memahami kebutuhan komunikasi."),
        ],
    ),
    (
        "gemini-untuk-produktivitas-dan-laporan",
        [
            ("mengenal-gemini", "Mengenal Gemini",
             "Gemini adalah asisten AI yang dapat membantu mengolah informasi dan menyiapkan draf pekerjaan. Sebelum menggunakan keluaran AI, perhatikan kerahasiaan data serta akurasi informasi.\n\nCoba tulis instruksi untuk merangkum catatan rapat menjadi keputusan dan daftar tindak lanjut.",
             "Apa yang harus diperhatikan saat memakai AI untuk pekerjaan?",
             ["Mengunggah semua data rahasia", "Tidak mengecek hasil", "Kerahasiaan dan ketepatan informasi", "Menghapus seluruh konteks"], "c",
             "Data sensitif dan keakuratan hasil harus diperhatikan."),
            ("merangkum-untuk-laporan", "Merangkum Informasi untuk Laporan",
             "Ringkasan yang bermanfaat membedakan fakta, temuan, dan tindakan yang perlu dilakukan. Kamu bisa meminta Gemini menghasilkan poin utama dari catatan yang telah disiapkan.\n\nPeriksa hasilnya dengan catatan asli sebelum memasukkannya ke laporan final.",
             "Apa langkah berikutnya setelah menerima ringkasan AI?",
             ["Memeriksa ringkasan dengan sumber", "Langsung memublikasikan", "Membuang catatan asli", "Menganggapnya pasti benar"], "a",
             "Validasi sumber membantu mencegah kesalahan dalam laporan."),
        ],
    ),
    (
        "notebooklm-untuk-belajar-dari-dokumen",
        [
            ("mengenal-notebooklm", "Mengenal NotebookLM",
             "NotebookLM membantu pengguna menjelajahi informasi dari sumber dokumen yang disediakan. Pengguna dapat mengajukan pertanyaan berdasarkan materi yang diunggah.\n\nSiapkan dokumen yang relevan, lalu mulai dengan pertanyaan yang spesifik dan periksa rujukan yang disajikan.",
             "Apa yang menjadi dasar analisis NotebookLM?",
             ["Dokumen sumber yang diberikan pengguna", "Ramalan acak", "Hanya riwayat pencarian", "Gambar tanpa konteks"], "a",
             "NotebookLM berfokus pada sumber yang dimasukkan pengguna."),
            ("mengajukan-pertanyaan-berbasis-sumber", "Bertanya Berdasarkan Sumber",
             "Pertanyaan yang spesifik membantu menemukan bagian penting dokumen. Misalnya, tanyakan tiga kesimpulan utama beserta dasar penjelasannya.\n\nBandingkan jawaban dengan sumber ketika diperlukan, terutama untuk angka, kutipan, dan kesimpulan penting.",
             "Cara memeriksa jawaban tentang dokumen adalah?",
             ["Menghindari sumber", "Mengulang jawaban tanpa membaca", "Membandingkan dengan dokumen yang dikutip", "Menganggap semua jawaban pasti benar"], "c",
             "Pemeriksaan dokumen asli penting untuk menjaga ketepatan informasi."),
        ],
    ),
]


def seed_lessons(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Lesson = apps.get_model("courses", "Lesson")
    QuizQuestion = apps.get_model("courses", "QuizQuestion")
    for course_slug, lessons in EXAMPLES:
        course = Course.objects.filter(slug=course_slug).first()
        if not course:
            continue
        for order, (slug, title, content, question, options, correct, explanation) in enumerate(lessons, 1):
            lesson, _ = Lesson.objects.get_or_create(
                course=course,
                slug=slug,
                defaults={
                    "title": title,
                    "summary": "Materi pengantar dan latihan singkat.",
                    "content": content,
                    "sort_order": order,
                    "is_published": True,
                },
            )
            if not QuizQuestion.objects.filter(lesson=lesson).exists():
                QuizQuestion.objects.create(
                    lesson=lesson, question=question,
                    option_a=options[0], option_b=options[1],
                    option_c=options[2], option_d=options[3],
                    correct_option=correct, explanation=explanation,
                )


class Migration(migrations.Migration):
    dependencies = [("courses", "0004_lesson_and_quiz")]

    operations = [
        migrations.RunPython(seed_lessons, migrations.RunPython.noop),
    ]
