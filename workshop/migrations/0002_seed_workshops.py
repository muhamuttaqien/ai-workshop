from datetime import date

from django.db import migrations


def seed_data(apps, schema_editor):
    Mentor = apps.get_model("workshop", "Mentor")
    Testimonial = apps.get_model("workshop", "Testimonial")
    Workshop = apps.get_model("workshop", "Workshop")

    mentor = Mentor.objects.create(
        name="Muhammad Angga Muttaqien",
        role="Co-Founder & CEO Indonesia AI",
        bio=(
            "Praktisi dan peneliti AI yang aktif mengembangkan teknologi Artificial "
            "Intelligence dan robotika, serta membagikan pendekatan praktis penggunaan "
            "AI untuk kebutuhan akademik dan profesional."
        ),
        photo="workshop/img/mentor.jpg",
    )

    testimonials = [
        ("Budi Kawira", "BK", "Marketing Product Development", "Telecommunications Industry", "Materinya menarik dan cukup mendalam, sehingga pengalaman belajarnya terasa lebih kaya daripada sekadar kelas pengantar."),
        ("Sumandi Ramadhan", "SR", "IT Implementor", "Tech Company", "Penjelasan mentor terasa terstruktur dan menarik, sehingga alur kerja dan proses membangun model AI menjadi lebih mudah dipahami."),
        ("Maria Amelia Suhardi", "MA", "General Practitioner", "RSUD Komodo", "Mentor menguasai bidangnya dan sangat membantu ketika peserta menemui kebuntuan selama proses belajar."),
        ("Yuan Shafira", "YS", "IT Business & System Analyst", "BOSSNET by Telkom Indonesia", "Materinya disusun bertahap dan dipadukan dengan banyak praktik, sehingga konsep yang dipelajari terasa lebih mudah dipahami dan diterapkan."),
        ("Cefiro Martha Y", "CM", "Process Engineer", "Wilmar Nabati Indonesia", "Programnya terasa lengkap karena materi, mentor, dan kesempatan membangun relasi berada dalam satu pengalaman belajar."),
        ("Teguh Prasetyo", "TP", "Head of R&D", "PT Triputra Agro Persada", "Bagi profesional di luar IT, belajar AI tetap relevan karena membantu memperkuat kemampuan analisis dan membuka cara pandang baru terhadap pekerjaan."),
    ]
    for idx, (name, initials, role, org, quote) in enumerate(testimonials, start=1):
        Testimonial.objects.create(
            name=name,
            initials=initials,
            role=role,
            organization=org,
            quote=quote,
            sort_order=idx,
        )

    Workshop.objects.create(
        slug="chatgpt-pendataan-harian",
        title="Pakai ChatGPT untuk Pendataan Harian",
        headline="Pakai ChatGPT",
        headline_accent="untuk Pendataan Harian",
        subtitle="Workshop praktis untuk mengubah catatan harian yang berantakan menjadi data yang lebih rapi dan siap direkap.",
        description=(
            "Belajar menggunakan ChatGPT untuk membantu proses pendataan harian, mulai dari "
            "mengubah catatan bebas menjadi format terstruktur, menjaga konsistensi data, "
            "sampai membuat ringkasan yang lebih cepat."
        ),
        meta_description="Workshop Pakai ChatGPT untuk Pendataan Harian oleh Indonesia AI, dilaksanakan 1 dan 3 Oktober 2026.",
        layout_variant="productivity",
        eyebrow="AI WORKSHOP • PRODUCTIVITY",
        audience_label="Untuk profesional, admin, operasional, UMKM, dan siapa pun yang rutin melakukan pendataan.",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 3),
        dates_label="1 & 3 Oktober 2026",
        days_label="Kamis & Sabtu",
        time_label="19.30–21.00 WIB",
        format_label="Online",
        duration_label="2 Sesi • Total 3 Jam",
        price_label="",
        registration_url="",
        show_registration=False,
        is_archived=True,
        hero_image="",
        hero_badge="CHATGPT + DAILY DATA",
        hero_flow="Chat → Struktur → Rekap",
        hero_note="Tidak perlu kemampuan programming",
        intro_title="Pendataan harian sering sederhana, tetapi pekerjaan merapikannya bisa memakan waktu.",
        intro_paragraphs=[
            "Catatan aktivitas, laporan singkat, chat tim, dan input lapangan sering datang dalam format yang tidak seragam.",
            "Di workshop ini, ChatGPT digunakan sebagai alat bantu untuk mengubah informasi tersebut menjadi data yang lebih terstruktur, konsisten, dan mudah direkap tanpa membuat proses kerja menjadi rumit.",
        ],
        outcomes=[
            {"number": "01", "title": "Ubah Chat Jadi Data", "text": "Ekstrak informasi penting dari catatan bebas menjadi field yang terstruktur."},
            {"number": "02", "title": "Standarkan Format", "text": "Bangun format pendataan yang konsisten meskipun input awal berbeda-beda."},
            {"number": "03", "title": "Percepat Rekap", "text": "Gunakan AI untuk membantu merangkum data harian dan menemukan hal yang perlu diperhatikan."},
            {"number": "04", "title": "Kurangi Copy-Paste", "text": "Buat workflow yang mengurangi pekerjaan manual berulang dalam proses pendataan."},
        ],
        audience_title="Untuk kamu yang bekerja dengan data harian, tetapi tidak ingin prosesnya terasa manual terus-menerus.",
        audience_intro="Fokusnya bukan coding, melainkan penggunaan ChatGPT sebagai alat bantu kerja sehari-hari.",
        audiences=[
            {"label": "Admin & Operations", "text": "Merapikan laporan, catatan, dan data rutin."},
            {"label": "Business & UMKM", "text": "Membantu pencatatan aktivitas, pelanggan, atau operasional."},
            {"label": "Project Team", "text": "Mengubah update tim menjadi rekap yang konsisten."},
            {"label": "Professional", "text": "Mengurangi pekerjaan repetitif dalam mengolah informasi harian."},
        ],
        curriculum_title="Dari chat yang berantakan menjadi data yang siap dipakai.",
        curriculum_intro="Dua sesi disusun mengikuti alur kerja nyata: memahami struktur data, lalu menerapkannya ke workflow pendataan dan rekap.",
        curriculum=[
            {
                "label": "SESI 01",
                "title": "Membangun Pendataan yang Terstruktur",
                "day": "Kamis",
                "time": "19.30–21.00 WIB",
                "modules": [
                    {"title": "Mengenali Pola Data Harian", "text": "Membedakan informasi utama, field, konteks, dan data yang perlu distandarkan."},
                    {"title": "Prompt untuk Ekstraksi Data", "text": "Mengubah teks bebas menjadi format tabel, daftar, atau struktur data yang konsisten."},
                    {"title": "Validasi dan Konsistensi", "text": "Mengecek field yang hilang, format yang tidak seragam, dan kemungkinan salah interpretasi."},
                ],
            },
            {
                "label": "SESI 02",
                "title": "Membuat Workflow Rekap Harian",
                "day": "Sabtu",
                "time": "19.30–21.00 WIB",
                "modules": [
                    {"title": "Dari Input ke Rekap", "text": "Menyusun langkah berulang dari input harian sampai ringkasan yang bisa dibaca cepat."},
                    {"title": "Summary dan Temuan Penting", "text": "Meminta ChatGPT menyoroti perubahan, anomali, atau informasi yang membutuhkan tindak lanjut."},
                    {"title": "Template untuk Pekerjaan Sendiri", "text": "Mengadaptasi workflow ke kebutuhan pendataan masing-masing peserta."},
                ],
            },
        ],
        benefits_title="Yang dibawa pulang setelah workshop",
        benefits_intro="Resource praktis untuk membantu menerapkan workflow yang sama pada pekerjaan sehari-hari.",
        benefits=[
            {"kicker": "LIVE", "title": "Workshop 2 Sesi", "text": "Belajar langsung dan mengikuti praktik dari awal sampai workflow jadi.", "visual": "live"},
            {"kicker": "PRAKTIK", "title": "Hands-on Pendataan", "text": "Latihan dengan contoh data harian yang dekat dengan pekerjaan nyata.", "visual": "practice"},
            {"kicker": "TEMPLATE", "title": "Template Pendataan Harian", "text": "Contoh struktur input dan output yang bisa disesuaikan ke kebutuhan sendiri.", "visual": "material"},
            {"kicker": "WORKFLOW", "title": "Chat-to-Table Workflow", "text": "Kerangka sederhana dari catatan bebas menuju data terstruktur dan rekap.", "visual": "flow"},
            {"kicker": "REPLAY", "title": "Rekaman Kelas", "text": "Materi dapat dipelajari kembali setelah workshop selesai.", "visual": "replay"},
            {"kicker": "BONUS", "title": "Belasan Modul Tools AI", "text": "Materi tambahan untuk memperluas penggunaan tools AI di pekerjaan.", "visual": "modules"},
        ],
        schedule_title="Dua sesi yang mengikuti alur kerja pendataan nyata.",
        schedule=[
            {"number": "01", "label": "KAMIS • 1 OKTOBER • 19.30–21.00 WIB", "title": "Membangun Data yang Terstruktur", "text": "Field, format, ekstraksi informasi, dan validasi hasil."},
            {"number": "02", "label": "SABTU • 3 OKTOBER • 19.30–21.00 WIB", "title": "Workflow Rekap Harian", "text": "Rekap, summary, temuan penting, dan adaptasi ke kebutuhan kerja."},
        ],
        mentor=mentor,
        mentor_section_title="Belajar langsung bersama praktisi yang menggunakan AI dalam pekerjaan nyata.",
        mentor_section_intro="Pendekatan workshop menekankan penggunaan AI yang praktis, terukur, dan mudah diadaptasi ke workflow masing-masing peserta.",
        registration_note="Workshop ini telah selesai dilaksanakan pada 1 dan 3 Oktober 2026.",
        faqs=[
            {"question": "Apakah workshop ini membutuhkan kemampuan coding?", "answer": "Tidak. Seluruh praktik berfokus pada penggunaan ChatGPT dan penyusunan workflow, bukan programming."},
            {"question": "Apa yang dimaksud dengan pendataan harian?", "answer": "Pendataan harian mencakup pencatatan aktivitas, laporan singkat, update operasional, data pelanggan, atau informasi rutin lain yang perlu dirapikan dan direkap."},
            {"question": "Apakah harus membawa data sendiri?", "answer": "Tidak. Workshop menggunakan contoh yang dapat diikuti semua peserta, kemudian workflow-nya dapat diadaptasi ke data masing-masing."},
            {"question": "Apakah ChatGPT berbayar wajib?", "answer": "Tidak harus. Konsep utama tetap dapat dipelajari dengan akun yang tersedia bagi peserta, meskipun kemampuan fitur dapat berbeda antar paket."},
            {"question": "Apakah peserta mendapatkan rekaman?", "answer": "Ya. Peserta workshop mendapatkan rekaman kelas dan materi pendukung yang disediakan untuk program tersebut."},
        ],
    )

    Workshop.objects.create(
        slug="claude-untuk-riset",
        title="Belajar Claude untuk Riset",
        headline="Belajar Claude",
        headline_accent="untuk Riset",
        subtitle="Untuk Mahasiswa Master & Doktoral",
        description=(
            "Workshop praktis untuk mahasiswa Master & Doktoral yang ingin menggunakan "
            "Claude sebagai partner riset untuk membaca paper, menelaah literatur, "
            "mempertajam ide, dan membangun argumentasi akademik."
        ),
        meta_description="Belajar Claude untuk Riset, workshop online praktis untuk mahasiswa Master, Doktoral, peneliti, dan akademisi pada 15 dan 16 Oktober 2026.",
        layout_variant="research",
        eyebrow="AI WORKSHOP • ONLINE",
        audience_label="Untuk Mahasiswa Master & Doktoral",
        start_date=date(2026, 10, 15),
        end_date=date(2026, 10, 16),
        dates_label="15 & 16 Oktober 2026",
        days_label="Kamis & Jumat",
        time_label="19.30–21.00 WIB",
        format_label="Online",
        duration_label="2 Hari • Total 3 Jam",
        price_label="Rp290.000",
        registration_url="",
        show_registration=True,
        is_archived=False,
        hero_image="workshop/img/hero.jpg",
        hero_badge="CLAUDE + RESEARCH",
        hero_flow="Paper → Compare → Gap → Writing",
        hero_note="Tidak perlu kemampuan programming",
        intro_title="Riset tidak harus selalu dimulai dari halaman kosong.",
        intro_paragraphs=[
            "Studi Master dan Doktoral berarti berhadapan dengan paper yang terus bertambah, ide yang berkembang, revisi berulang, dan pertanyaan penelitian yang belum tentu langsung menemukan jawabannya.",
            "Claude dapat membantu mempercepat sebagian proses tersebut. Bukan untuk menggantikan peneliti, tetapi untuk membantu kamu membaca lebih efektif, mengeksplorasi lebih luas, dan berpikir lebih terstruktur.",
        ],
        outcomes=[
            {"number": "01", "title": "Memahami Paper", "text": "Bongkar struktur paper, metode, asumsi, kontribusi, dan keterbatasannya."},
            {"number": "02", "title": "Menelaah Literatur", "text": "Bandingkan banyak sumber dan petakan hubungan antar ide secara sistematis."},
            {"number": "03", "title": "Mempertajam Ide", "text": "Gunakan AI untuk menguji asumsi, mengembangkan pertanyaan, dan menemukan celah argumen."},
            {"number": "04", "title": "Mengembangkan Tulisan", "text": "Bangun outline, cek alur argumentasi, dan lakukan revisi secara iteratif."},
        ],
        audience_title="Dirancang untuk peneliti yang ingin bekerja lebih efektif dengan AI.",
        audience_intro="Tidak harus berasal dari bidang Computer Science atau Artificial Intelligence.",
        audiences=[
            {"icon": "M", "label": "Mahasiswa Master", "text": "Untuk tesis, literature review, eksplorasi topik, dan penyusunan argumentasi."},
            {"icon": "D", "label": "Mahasiswa Doktoral", "text": "Untuk mengelola literatur yang kompleks dan memperdalam novelty penelitian."},
            {"icon": "R", "label": "Peneliti & Akademisi", "text": "Untuk membaca, membandingkan, mengkritisi, dan mengembangkan karya ilmiah."},
            {"icon": "P", "label": "Calon Pascasarjana", "text": "Untuk membantu eksplorasi awal topik dan mempersiapkan ide proposal penelitian."},
        ],
        curriculum_title="Dua hari untuk membangun workflow riset yang lebih cerdas.",
        curriculum_intro="Fokus workshop bukan menghafal prompt, tetapi memahami pola kerja yang bisa digunakan kembali untuk berbagai kebutuhan riset.",
        curriculum=[
            {
                "label": "DAY 01",
                "title": "Claude untuk Memahami & Mengeksplorasi Riset",
                "day": "Kamis",
                "time": "19.30–21.00 WIB",
                "modules": [
                    {"number": "01", "title": "Claude sebagai Research Assistant", "text": "Memahami kemampuan, keterbatasan, konteks, dan cara berinteraksi dengan AI dalam pekerjaan akademik."},
                    {"number": "02", "title": "Membaca Paper Lebih Efektif", "text": "Membedah metode, kontribusi, asumsi, hasil, dan keterbatasan penelitian tanpa berhenti pada summary."},
                    {"number": "03", "title": "Literature Review dengan AI", "text": "Mengelompokkan literatur, membandingkan pendekatan, menemukan pola, dan mengidentifikasi gap potensial."},
                ],
            },
            {
                "label": "DAY 02",
                "title": "Claude untuk Mengembangkan & Menulis Riset",
                "day": "Jumat",
                "time": "19.30–21.00 WIB",
                "modules": [
                    {"number": "04", "title": "Research Question & Ide Penelitian", "text": "Mempersempit topik, menguji asumsi, mencari counterargument, dan mempertajam kontribusi riset."},
                    {"number": "05", "title": "Argumentasi & Academic Writing", "text": "Membangun outline, memeriksa logical gap, mengkritik draft, dan memperjelas penjelasan teknis."},
                    {"number": "06", "title": "Personal AI Research Workflow", "text": "Menggabungkan teknik workshop menjadi workflow yang bisa diadaptasi ke riset masing-masing."},
                ],
            },
        ],
        benefits_title="Apa yang akan kamu dapatkan?",
        benefits_intro="Bukan hanya sesi kelas, tetapi rangkaian resource yang bisa terus digunakan setelah workshop selesai.",
        benefits=[
            {"number": "01", "kicker": "LIVE LEARNING", "title": "Live Workshop 2 Hari", "text": "Belajar langsung dalam dua sesi intensif bersama mentor, dengan ruang untuk bertanya dan mendiskusikan konteks risetmu.", "visual": "live"},
            {"number": "02", "kicker": "PRACTICE", "title": "Hands-on Practice", "text": "Tidak berhenti di teori. Kamu akan langsung mencoba cara menggunakan Claude untuk membaca, membandingkan, mengkritisi, dan mengembangkan materi riset.", "visual": "practice"},
            {"number": "03", "kicker": "MATERIAL", "title": "Materi Workshop", "text": "Materi terstruktur yang dapat digunakan kembali sebagai referensi saat kamu menerapkan workflow AI pada penelitianmu sendiri.", "visual": "material"},
            {"number": "04", "kicker": "TEMPLATE", "title": "Research Workflow Template", "text": "Gunakan kerangka praktis untuk bergerak dari paper menuju pemahaman, perbandingan, research gap, research question, hingga argumentasi.", "visual": "flow"},
            {"number": "05", "kicker": "REPLAY", "title": "Rekaman Kelas", "text": "Pelajari kembali pembahasan workshop setelah sesi selesai dan gunakan rekamannya untuk mengulang bagian yang paling relevan dengan kebutuhanmu.", "visual": "replay"},
            {"number": "06", "kicker": "BONUS LEARNING", "title": "Belasan Modul Tools AI", "text": "Dapatkan materi tambahan untuk mengenal berbagai tools AI yang dapat mendukung produktivitas, pembelajaran, dan workflow riset.", "visual": "modules"},
        ],
        schedule_title="3 jam pembelajaran, dibagi dalam dua sesi intensif.",
        schedule=[
            {"number": "01", "label": "KAMIS • 15 OKTOBER • 19.30–21.00 WIB", "title": "Memahami & Mengeksplorasi Riset", "text": "Research assistant, paper understanding, literature review, comparison, dan research gap."},
            {"number": "02", "label": "JUMAT • 16 OKTOBER • 19.30–21.00 WIB", "title": "Mengembangkan & Menulis Riset", "text": "Research question, brainstorming, critique, argumentasi, academic writing, dan personal workflow."},
        ],
        mentor=mentor,
        mentor_section_title="Belajar langsung bersama praktisi yang memahami proses riset dan AI.",
        mentor_section_intro="Mentor akan membawa contoh praktis penggunaan AI dalam membaca, mengevaluasi, dan mengembangkan penelitian.",
        registration_note="Materi + rekaman + belasan modul tools AI termasuk",
        faqs=[
            {"question": "Apakah workshop hanya untuk mahasiswa Master dan Doktoral?", "answer": "Fokus utamanya memang mahasiswa Master dan Doktoral, tetapi calon mahasiswa pascasarjana, peneliti, dosen, dan akademisi tetap dapat mengikuti workshop."},
            {"question": "Apakah saya harus bisa coding?", "answer": "Tidak. Workshop ini tidak membutuhkan kemampuan programming."},
            {"question": "Apakah harus sudah memiliki topik penelitian?", "answer": "Tidak. Peserta yang masih dalam tahap eksplorasi topik juga dapat mengikuti workshop."},
            {"question": "Apakah workshop mengajarkan AI untuk menulis tesis secara otomatis?", "answer": "Tidak. Fokus workshop adalah menggunakan AI untuk membantu proses membaca, berpikir, mengembangkan argumentasi, dan revisi, sementara tanggung jawab akademik tetap berada pada peneliti."},
            {"question": "Apakah peserta mendapatkan rekaman dan modul tools AI?", "answer": "Ya. Peserta mendapatkan rekaman kelas serta akses ke belasan modul tambahan tentang tools AI."},
            {"question": "Apakah harus menggunakan Claude versi berbayar?", "answer": "Tidak harus. Konsep dan workflow utama tetap dapat dipelajari menggunakan akun Claude yang tersedia bagi peserta, meskipun beberapa fitur tertentu dapat bergantung pada paket yang digunakan."},
        ],
    )


def reverse_seed(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Testimonial = apps.get_model("workshop", "Testimonial")
    Mentor = apps.get_model("workshop", "Mentor")
    Workshop.objects.filter(slug__in=["chatgpt-pendataan-harian", "claude-untuk-riset"]).delete()
    Testimonial.objects.all().delete()
    Mentor.objects.filter(name="Muhammad Angga Muttaqien").delete()


class Migration(migrations.Migration):

    dependencies = [("workshop", "0001_initial")]

    operations = [migrations.RunPython(seed_data, reverse_seed)]
