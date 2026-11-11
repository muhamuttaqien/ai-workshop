from datetime import date

from django.db import migrations


MODULES_TEXT = (
    "Belasan modul tambahan tentang tools AI seperti ChatGPT, Claude, Gemini, "
    "Perplexity dan lainnya."
)


def add_related_content(
    workshop,
    WorkshopIntroParagraph,
    WorkshopOutcome,
    WorkshopAudience,
    WorkshopCurriculumModule,
    WorkshopBenefit,
    WorkshopScheduleItem,
    WorkshopFAQ,
    *,
    intros,
    outcomes,
    audiences,
    modules,
    benefits,
    schedule,
    faqs,
):
    for idx, text in enumerate(intros, start=1):
        WorkshopIntroParagraph.objects.create(
            workshop=workshop,
            text=text,
            sort_order=idx,
        )

    for idx, (number, title, text) in enumerate(outcomes, start=1):
        WorkshopOutcome.objects.create(
            workshop=workshop,
            number=number,
            title=title,
            text=text,
            sort_order=idx,
        )

    for idx, (icon, label, text) in enumerate(audiences, start=1):
        WorkshopAudience.objects.create(
            workshop=workshop,
            icon=icon,
            label=label,
            text=text,
            sort_order=idx,
        )

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

    for idx, (number, label, title, text) in enumerate(schedule, start=1):
        WorkshopScheduleItem.objects.create(
            workshop=workshop,
            number=number,
            label=label,
            title=title,
            text=text,
            sort_order=idx,
        )

    for idx, (question, answer) in enumerate(faqs, start=1):
        WorkshopFAQ.objects.create(
            workshop=workshop,
            question=question,
            answer=answer,
            sort_order=idx,
        )


def seed_new_workshops(apps, schema_editor):
    Mentor = apps.get_model("workshop", "Mentor")
    Workshop = apps.get_model("workshop", "Workshop")
    WorkshopIntroParagraph = apps.get_model("workshop", "WorkshopIntroParagraph")
    WorkshopOutcome = apps.get_model("workshop", "WorkshopOutcome")
    WorkshopAudience = apps.get_model("workshop", "WorkshopAudience")
    WorkshopCurriculumModule = apps.get_model("workshop", "WorkshopCurriculumModule")
    WorkshopBenefit = apps.get_model("workshop", "WorkshopBenefit")
    WorkshopScheduleItem = apps.get_model("workshop", "WorkshopScheduleItem")
    WorkshopFAQ = apps.get_model("workshop", "WorkshopFAQ")

    mentor, _ = Mentor.objects.get_or_create(
        name="Muhammad Angga Muttaqien",
        defaults={
            "role": "Co-Founder & CEO Indonesia AI",
            "bio": (
                "Praktisi dan peneliti AI yang aktif mengembangkan teknologi Artificial "
                "Intelligence dan robotika, serta membagikan pendekatan praktis penggunaan "
                "AI untuk kebutuhan akademik dan profesional."
            ),
            "photo": "workshop/img/mentor.jpg",
        },
    )

    canva = Workshop.objects.create(
        slug="canva-ai-konten-media-sosial",
        title="Pakai Canva AI untuk Membuat Konten Media Sosial",
        headline="Pakai Canva AI",
        headline_accent="untuk Konten Media Sosial",
        subtitle="Dari ide ke visual yang siap dipublikasikan.",
        description=(
            "Workshop praktis untuk membuat workflow konten media sosial dengan Canva AI, "
            "mulai dari mengembangkan ide, menyusun visual, menjaga konsistensi desain, "
            "hingga menghasilkan variasi konten yang siap digunakan."
        ),
        meta_description=(
            "Workshop Canva AI untuk membuat konten media sosial secara praktis, "
            "19 dan 20 November 2026."
        ),
        layout_variant="showcase",
        eyebrow="AI WORKSHOP • CREATIVE",
        audience_label="Untuk creator, marketing, UMKM, social media team, dan profesional non-desainer.",
        start_date=date(2026, 11, 19),
        end_date=date(2026, 11, 20),
        dates_label="19 & 20 November 2026",
        days_label="Kamis & Jumat",
        time_label="19.30–21.00 WIB",
        format_label="Zoom Online",
        duration_label="2 Hari • Total 3 Jam (Live) + 6 Jam (Online)",
        original_price_label="Rp780.000",
        price_label="Rp390.000",
        discount_label="50% OFF",
        registration_url="",
        show_registration=True,
        is_archived=False,
        is_published=True,
        hero_image="",
        hero_badge="CANVA AI + SOCIAL CONTENT",
        hero_flow="Idea → Create → Refine → Publish",
        hero_note="Tidak perlu kemampuan desain profesional",
        intro_title="Membuat konten rutin tidak harus selalu dimulai dari kanvas kosong.",
        audience_title="Cocok untuk siapa pun yang perlu membuat visual secara rutin.",
        audience_intro="Fokus workshop adalah workflow praktis, bukan teori desain yang kompleks.",
        curriculum_title="Dua sesi dari ide sampai konten siap dipublikasikan.",
        curriculum_intro=(
            "Peserta belajar membangun alur kerja yang dapat diulang untuk menghasilkan "
            "konten visual dengan lebih cepat dan konsisten."
        ),
        benefits_title="Apa yang akan kamu dapatkan?",
        benefits_intro="Template, praktik, dan resource yang dapat langsung dipakai setelah workshop.",
        schedule_title="Dua sesi untuk membangun workflow konten visual yang praktis.",
        mentor=mentor,
        mentor_section_title="Belajar menggunakan AI sebagai partner dalam proses kreatif.",
        mentor_section_intro=(
            "Workshop menekankan cara menggabungkan ide, AI, dan keputusan visual manusia "
            "agar hasil tetap relevan dan mudah diterapkan."
        ),
        registration_note="Materi + rekaman + belasan modul tools AI termasuk",
    )

    add_related_content(
        canva,
        WorkshopIntroParagraph,
        WorkshopOutcome,
        WorkshopAudience,
        WorkshopCurriculumModule,
        WorkshopBenefit,
        WorkshopScheduleItem,
        WorkshopFAQ,
        intros=[
            "Produksi konten media sosial sering terasa repetitif: mencari ide, memilih layout, menyesuaikan format, lalu membuat variasi untuk kanal yang berbeda.",
            "Di workshop ini, Canva AI digunakan untuk membantu mempercepat proses tersebut tanpa menghilangkan kontrol kreatif dari pengguna.",
        ],
        outcomes=[
            ("01", "Kembangkan Ide", "Mengubah brief sederhana menjadi beberapa arah konten yang dapat dieksplorasi."),
            ("02", "Bangun Visual", "Menggunakan fitur AI Canva untuk mempercepat pembuatan draft visual."),
            ("03", "Jaga Konsistensi", "Menyusun sistem visual agar variasi konten tetap terasa satu brand."),
            ("04", "Buat Banyak Format", "Mengadaptasi satu ide menjadi beberapa ukuran dan kebutuhan publikasi."),
        ],
        audiences=[
            ("C", "Content Creator", "Membuat konten lebih cepat tanpa kehilangan ruang untuk eksplorasi."),
            ("M", "Marketing Team", "Mengembangkan visual campaign dan konten rutin dengan workflow yang lebih efisien."),
            ("U", "UMKM & Business Owner", "Membuat materi promosi tanpa selalu bergantung pada proses desain yang panjang."),
            ("P", "Professional", "Membuat visual untuk edukasi, komunikasi, atau personal branding."),
        ],
        modules=[
            ("day-01", "DAY 01", "Dari Brief ke Konsep Visual", "Kamis", "19.30–21.00 WIB", "01", "Membaca Brief Konten", "Menentukan tujuan, audiens, pesan utama, dan output visual yang dibutuhkan."),
            ("day-01", "DAY 01", "Dari Brief ke Konsep Visual", "Kamis", "19.30–21.00 WIB", "02", "Mengembangkan Ide dengan AI", "Menghasilkan beberapa arah konten dan memilih konsep yang paling relevan."),
            ("day-01", "DAY 01", "Dari Brief ke Konsep Visual", "Kamis", "19.30–21.00 WIB", "03", "Membangun Draft Visual", "Menggunakan fitur AI dan template untuk membuat draft awal lebih cepat."),
            ("day-02", "DAY 02", "Dari Draft ke Konten Siap Pakai", "Jumat", "19.30–21.00 WIB", "04", "Refinement & Consistency", "Merapikan hierarchy, copy, spacing, dan elemen visual agar hasil lebih konsisten."),
            ("day-02", "DAY 02", "Dari Draft ke Konten Siap Pakai", "Jumat", "19.30–21.00 WIB", "05", "Variasi Format Konten", "Mengadaptasi konsep yang sama ke berbagai ukuran dan kebutuhan platform."),
            ("day-02", "DAY 02", "Dari Draft ke Konten Siap Pakai", "Jumat", "19.30–21.00 WIB", "06", "Personal Content Workflow", "Menyusun alur kerja yang dapat digunakan kembali untuk produksi konten berikutnya."),
        ],
        benefits=[
            ("01", "LIVE LEARNING", "Live Workshop 2 Hari", "Belajar langsung dalam dua sesi interaktif bersama mentor.", "live"),
            ("02", "PRACTICE", "Hands-on Creative Practice", "Langsung membuat dan menyempurnakan visual selama workshop.", "practice"),
            ("03", "MATERIAL", "Materi Workshop", "Materi terstruktur yang dapat digunakan kembali sebagai referensi.", "material"),
            ("04", "TEMPLATE", "Content Workflow Template", "Kerangka dari brief menuju ide, visual, refinement, dan publikasi.", "flow"),
            ("05", "REPLAY", "Rekaman Kelas", "Pelajari kembali pembahasan dan demo setelah sesi selesai.", "replay"),
            ("06", "BONUS LEARNING", "Belasan Modul Tools AI", MODULES_TEXT, "modules"),
        ],
        schedule=[
            ("01", "KAMIS • 19 NOVEMBER • 19.30–21.00 WIB", "Dari Brief ke Konsep Visual", "Brief, ide, arah visual, dan pembuatan draft."),
            ("02", "JUMAT • 20 NOVEMBER • 19.30–21.00 WIB", "Dari Draft ke Konten Siap Pakai", "Refinement, konsistensi, variasi format, dan workflow pribadi."),
        ],
        faqs=[
            ("Apakah harus bisa desain?", "Tidak. Workshop dirancang agar dapat diikuti peserta tanpa latar belakang desain profesional."),
            ("Apakah harus menggunakan Canva Pro?", "Tidak harus. Konsep utama tetap dapat dipelajari dengan fitur yang tersedia pada akun peserta."),
            ("Apakah workshop ini hanya untuk social media manager?", "Tidak. Materinya juga relevan untuk UMKM, creator, marketing, dan profesional yang perlu membuat visual sendiri."),
            ("Apakah mendapatkan rekaman?", "Ya. Peserta mendapatkan rekaman kelas untuk dipelajari kembali."),
            ("Apakah mendapatkan materi tambahan?", MODULES_TEXT),
        ],
    )

    gamma = Workshop.objects.create(
        slug="gamma-presentasi-profesional",
        title="Pakai Gamma untuk Membuat Presentasi Profesional",
        headline="Pakai Gamma",
        headline_accent="untuk Presentasi Profesional",
        subtitle="Dari brief ke deck yang jelas, visual, dan siap dipresentasikan.",
        description=(
            "Workshop praktis untuk menggunakan Gamma dalam menyusun struktur, narasi, "
            "dan visual presentasi profesional, mulai dari brief awal hingga deck yang "
            "lebih siap digunakan untuk pekerjaan."
        ),
        meta_description=(
            "Workshop Gamma untuk membuat presentasi profesional secara praktis, "
            "3 dan 4 Desember 2026."
        ),
        layout_variant="showcase",
        eyebrow="AI WORKSHOP • PRESENTATION",
        audience_label="Untuk profesional, business, sales, project team, educator, dan siapa pun yang rutin membuat presentasi.",
        start_date=date(2026, 12, 3),
        end_date=date(2026, 12, 4),
        dates_label="3 & 4 Desember 2026",
        days_label="Kamis & Jumat",
        time_label="19.30–21.00 WIB",
        format_label="Zoom Online",
        duration_label="2 Hari • Total 3 Jam (Live) + 6 Jam (Online)",
        original_price_label="Rp780.000",
        price_label="Rp390.000",
        discount_label="50% OFF",
        registration_url="",
        show_registration=True,
        is_archived=False,
        is_published=True,
        hero_image="",
        hero_badge="GAMMA + PRESENTATION",
        hero_flow="Brief → Story → Visual → Present",
        hero_note="Fokus pada struktur dan komunikasi, bukan dekorasi semata",
        intro_title="Presentasi yang baik dimulai dari cerita yang jelas, bukan dari memilih template.",
        audience_title="Untuk kamu yang sering perlu menjelaskan ide melalui slide.",
        audience_intro="Cocok untuk kebutuhan internal, proposal, edukasi, maupun komunikasi bisnis.",
        curriculum_title="Bangun deck dari pesan utama sampai visual yang siap dipresentasikan.",
        curriculum_intro=(
            "Dua sesi mengikuti proses nyata pembuatan presentasi: membangun narrative flow, "
            "lalu mengubahnya menjadi deck yang lebih ringkas dan visual."
        ),
        benefits_title="Apa yang akan kamu dapatkan?",
        benefits_intro="Resource praktis untuk membuat presentasi berikutnya dengan workflow yang lebih cepat.",
        schedule_title="Dua sesi dari brief ke deck siap presentasi.",
        mentor=mentor,
        mentor_section_title="Belajar menyusun presentasi dengan bantuan AI tanpa kehilangan kontrol atas pesan.",
        mentor_section_intro=(
            "Fokusnya adalah membuat AI membantu proses berpikir dan produksi, "
            "sementara keputusan komunikasi tetap berada pada pembuat presentasi."
        ),
        registration_note="Materi + rekaman + belasan modul tools AI termasuk",
    )

    add_related_content(
        gamma,
        WorkshopIntroParagraph,
        WorkshopOutcome,
        WorkshopAudience,
        WorkshopCurriculumModule,
        WorkshopBenefit,
        WorkshopScheduleItem,
        WorkshopFAQ,
        intros=[
            "Membuat slide sering memakan waktu bukan karena kurangnya template, tetapi karena pesan utama dan alur ceritanya belum benar-benar jelas.",
            "Gamma dapat membantu mempercepat proses dari brief menuju struktur dan visual, selama pengguna tetap mengarahkan narasi dan keputusan akhirnya.",
        ],
        outcomes=[
            ("01", "Susun Storyline", "Mengubah brief menjadi alur presentasi yang lebih mudah diikuti."),
            ("02", "Bangun Deck", "Menghasilkan draft presentasi dengan struktur yang lebih cepat."),
            ("03", "Perbaiki Visual", "Menyederhanakan isi dan menyeimbangkan teks, visual, serta hierarchy."),
            ("04", "Siapkan Presentasi", "Merapikan deck agar lebih siap untuk disampaikan kepada audiens."),
        ],
        audiences=[
            ("B", "Business & Management", "Untuk proposal, update, dan komunikasi strategis."),
            ("S", "Sales & Marketing", "Untuk pitch, campaign, dan materi komunikasi pelanggan."),
            ("P", "Project Team", "Untuk project update, review, dan stakeholder communication."),
            ("E", "Educator & Professional", "Untuk training, sharing, dan presentasi berbasis pengetahuan."),
        ],
        modules=[
            ("day-01", "DAY 01", "Membangun Narrative Flow", "Kamis", "19.30–21.00 WIB", "01", "Dari Brief ke Pesan Utama", "Mengidentifikasi tujuan presentasi, audiens, dan satu pesan utama yang ingin dibawa pulang."),
            ("day-01", "DAY 01", "Membangun Narrative Flow", "Kamis", "19.30–21.00 WIB", "02", "Menyusun Storyline", "Membangun urutan masalah, insight, solusi, dan next action yang lebih mudah dipahami."),
            ("day-01", "DAY 01", "Membangun Narrative Flow", "Kamis", "19.30–21.00 WIB", "03", "Generate Draft dengan Gamma", "Menggunakan Gamma untuk mengubah outline menjadi draft deck dengan cepat."),
            ("day-02", "DAY 02", "Menyempurnakan Deck", "Jumat", "19.30–21.00 WIB", "04", "Edit untuk Kejelasan", "Mengurangi teks, memperkuat hierarchy, dan memastikan setiap slide punya fungsi."),
            ("day-02", "DAY 02", "Menyempurnakan Deck", "Jumat", "19.30–21.00 WIB", "05", "Visual & Supporting Evidence", "Memilih visual, data, dan elemen pendukung yang membantu pesan utama."),
            ("day-02", "DAY 02", "Menyempurnakan Deck", "Jumat", "19.30–21.00 WIB", "06", "Presentation-ready Workflow", "Menyusun checklist akhir dan workflow yang dapat dipakai kembali."),
        ],
        benefits=[
            ("01", "LIVE LEARNING", "Live Workshop 2 Hari", "Belajar langsung dalam dua sesi interaktif bersama mentor.", "live"),
            ("02", "PRACTICE", "Hands-on Deck Building", "Langsung membangun dan memperbaiki deck menggunakan Gamma.", "practice"),
            ("03", "MATERIAL", "Materi Workshop", "Materi terstruktur yang dapat digunakan kembali saat membuat presentasi.", "material"),
            ("04", "TEMPLATE", "Presentation Workflow Template", "Kerangka dari brief menuju storyline, draft, refinement, dan final deck.", "flow"),
            ("05", "REPLAY", "Rekaman Kelas", "Pelajari kembali pembahasan dan demo setelah sesi selesai.", "replay"),
            ("06", "BONUS LEARNING", "Belasan Modul Tools AI", MODULES_TEXT, "modules"),
        ],
        schedule=[
            ("01", "KAMIS • 3 DESEMBER • 19.30–21.00 WIB", "Membangun Narrative Flow", "Tujuan, audiens, pesan utama, storyline, dan draft awal."),
            ("02", "JUMAT • 4 DESEMBER • 19.30–21.00 WIB", "Menyempurnakan Deck", "Editing, visual, evidence, dan presentation-ready workflow."),
        ],
        faqs=[
            ("Apakah harus punya pengalaman desain presentasi?", "Tidak. Workshop dimulai dari struktur komunikasi dan workflow yang mudah diikuti."),
            ("Apakah Gamma wajib berbayar?", "Tidak harus. Peserta dapat mengikuti konsep utama dengan akun yang tersedia bagi masing-masing peserta."),
            ("Apakah cocok untuk presentasi akademik?", "Ya. Prinsip storyline dan penyederhanaan informasi juga relevan untuk presentasi akademik dan edukasi."),
            ("Apakah mendapatkan rekaman?", "Ya. Peserta mendapatkan rekaman kelas untuk dipelajari kembali."),
            ("Apakah mendapatkan materi tambahan?", MODULES_TEXT),
        ],
    )

    notebooklm = Workshop.objects.create(
        slug="notebooklm-belajar-dari-dokumen",
        title="Belajar NotebookLM untuk Belajar dari Dokumen",
        headline="Belajar NotebookLM",
        headline_accent="untuk Belajar dari Dokumen",
        subtitle="Bangun cara belajar yang lebih terstruktur dari PDF, catatan, dan materi sendiri.",
        description=(
            "Workshop beginner-friendly untuk menggunakan NotebookLM sebagai pendamping belajar "
            "berbasis sumber sendiri, mulai dari memasukkan dokumen, bertanya secara terarah, "
            "membuat rangkuman, sampai membangun workflow belajar yang dapat digunakan kembali."
        ),
        meta_description=(
            "Workshop beginner-friendly NotebookLM untuk belajar dari dokumen, "
            "17 dan 18 Desember 2026."
        ),
        layout_variant="guide",
        eyebrow="AI WORKSHOP • BEGINNER GUIDE",
        audience_label="Untuk mahasiswa, pelajar, profesional, educator, dan siapa pun yang belajar dari banyak dokumen.",
        start_date=date(2026, 12, 17),
        end_date=date(2026, 12, 18),
        dates_label="17 & 18 Desember 2026",
        days_label="Kamis & Jumat",
        time_label="19.30–21.00 WIB",
        format_label="Zoom Online",
        duration_label="2 Hari • Total 3 Jam (Live) + 6 Jam (Online)",
        original_price_label="Rp780.000",
        price_label="Rp390.000",
        discount_label="50% OFF",
        registration_url="",
        show_registration=True,
        is_archived=False,
        is_published=True,
        hero_image="",
        hero_badge="NOTEBOOKLM • GETTING STARTED",
        hero_flow="Upload → Ask → Understand → Review",
        hero_note="Cocok untuk pemula dan tidak membutuhkan kemampuan coding",
        intro_title="AI akan jauh lebih berguna ketika bekerja dari sumber yang memang ingin kamu pelajari.",
        audience_title="Dirancang untuk siapa pun yang belajar dari dokumen.",
        audience_intro="Mulai dari PDF kuliah sampai dokumen kerja, tanpa perlu workflow teknis yang rumit.",
        curriculum_title="Mulai dari nol sampai punya workflow belajar sendiri.",
        curriculum_intro=(
            "Workshop disusun seperti panduan langkah demi langkah: memahami sumber, "
            "bertanya dengan baik, lalu mengubah hasilnya menjadi proses belajar aktif."
        ),
        benefits_title="Apa yang akan kamu dapatkan?",
        benefits_intro="Panduan dan resource yang mudah diterapkan kembali pada materi belajar lain.",
        schedule_title="Dua sesi untuk membangun kebiasaan belajar berbasis sumber.",
        mentor=mentor,
        mentor_section_title="Belajar menggunakan AI sebagai pendamping belajar, bukan pengganti proses memahami.",
        mentor_section_intro=(
            "Pendekatan workshop berfokus pada cara bertanya, memeriksa sumber, "
            "dan menggunakan AI untuk membuat proses belajar lebih aktif."
        ),
        registration_note="Materi + rekaman + belasan modul tools AI termasuk",
    )

    add_related_content(
        notebooklm,
        WorkshopIntroParagraph,
        WorkshopOutcome,
        WorkshopAudience,
        WorkshopCurriculumModule,
        WorkshopBenefit,
        WorkshopScheduleItem,
        WorkshopFAQ,
        intros=[
            "Saat materi belajar semakin banyak, masalahnya sering bukan kekurangan informasi, tetapi sulit menemukan bagian penting dan menghubungkannya satu sama lain.",
            "NotebookLM membantu bekerja dari sumber yang kita pilih sendiri sehingga proses bertanya, merangkum, dan meninjau materi dapat lebih terarah.",
        ],
        outcomes=[
            ("01", "Siapkan Sumber", "Mengorganisasi dokumen yang ingin dipelajari ke dalam satu notebook."),
            ("02", "Ajukan Pertanyaan", "Membuat pertanyaan yang membantu memahami konsep, bukan hanya meminta ringkasan."),
            ("03", "Bangun Pemahaman", "Menghubungkan informasi dari beberapa bagian atau sumber."),
            ("04", "Review Aktif", "Mengubah materi menjadi pertanyaan, checklist, atau rangkuman untuk belajar ulang."),
        ],
        audiences=[
            ("M", "Mahasiswa", "Untuk memahami PDF, paper, slide, dan materi kuliah."),
            ("P", "Pelajar & Learner", "Untuk belajar mandiri dari sumber yang sudah dimiliki."),
            ("R", "Professional", "Untuk memahami dokumen kerja, guideline, dan materi internal."),
            ("E", "Educator", "Untuk menavigasi materi dan menyiapkan aktivitas belajar berbasis sumber."),
        ],
        modules=[
            ("day-01", "DAY 01", "Memulai dengan NotebookLM", "Kamis", "19.30–21.00 WIB", "01", "Mengenal Source-based AI", "Memahami perbedaan bekerja dari sumber sendiri dibanding meminta jawaban AI secara umum."),
            ("day-01", "DAY 01", "Memulai dengan NotebookLM", "Kamis", "19.30–21.00 WIB", "02", "Menyiapkan Notebook & Sources", "Mengorganisasi PDF, catatan, dan dokumen agar mudah digunakan selama belajar."),
            ("day-01", "DAY 01", "Memulai dengan NotebookLM", "Kamis", "19.30–21.00 WIB", "03", "Bertanya untuk Memahami", "Membuat pertanyaan yang membantu menjelaskan konsep, contoh, hubungan, dan bagian yang membingungkan."),
            ("day-02", "DAY 02", "Membangun Workflow Belajar", "Jumat", "19.30–21.00 WIB", "04", "Compare & Connect", "Membandingkan sumber dan menemukan hubungan antarkonsep secara lebih terstruktur."),
            ("day-02", "DAY 02", "Membangun Workflow Belajar", "Jumat", "19.30–21.00 WIB", "05", "Active Review", "Mengubah materi menjadi pertanyaan latihan, rangkuman, dan poin review."),
            ("day-02", "DAY 02", "Membangun Workflow Belajar", "Jumat", "19.30–21.00 WIB", "06", "Personal Learning Workflow", "Menyusun langkah yang dapat dipakai kembali untuk topik dan dokumen lain."),
        ],
        benefits=[
            ("01", "LIVE LEARNING", "Live Workshop 2 Hari", "Belajar langkah demi langkah dalam dua sesi bersama mentor.", "live"),
            ("02", "PRACTICE", "Hands-on Learning", "Langsung mencoba NotebookLM menggunakan contoh dokumen selama workshop.", "practice"),
            ("03", "MATERIAL", "Materi Workshop", "Panduan yang dapat digunakan kembali saat belajar dari dokumen lain.", "material"),
            ("04", "TEMPLATE", "Learning Workflow Template", "Kerangka sederhana dari upload sumber sampai review aktif.", "flow"),
            ("05", "REPLAY", "Rekaman Kelas", "Pelajari kembali setiap langkah setelah workshop selesai.", "replay"),
            ("06", "BONUS LEARNING", "Belasan Modul Tools AI", MODULES_TEXT, "modules"),
        ],
        schedule=[
            ("01", "KAMIS • 17 DESEMBER • 19.30–21.00 WIB", "Memulai dengan NotebookLM", "Source-based AI, menyiapkan notebook, dan bertanya untuk memahami."),
            ("02", "JUMAT • 18 DESEMBER • 19.30–21.00 WIB", "Membangun Workflow Belajar", "Compare, connect, active review, dan personal learning workflow."),
        ],
        faqs=[
            ("Apakah workshop ini cocok untuk pemula?", "Ya. Workshop dirancang sebagai panduan langkah demi langkah dan tidak membutuhkan pengalaman AI sebelumnya."),
            ("Apakah harus bisa coding?", "Tidak. Seluruh praktik dilakukan melalui antarmuka NotebookLM."),
            ("Dokumen seperti apa yang bisa digunakan?", "Workshop akan membahas penggunaan dokumen belajar seperti PDF, catatan, slide, dan sumber lain yang didukung oleh NotebookLM."),
            ("Apakah mendapatkan rekaman?", "Ya. Peserta mendapatkan rekaman kelas untuk dipelajari kembali."),
            ("Apakah mendapatkan materi tambahan?", MODULES_TEXT),
        ],
    )


def remove_new_workshops(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")
    Workshop.objects.filter(
        slug__in=[
            "canva-ai-konten-media-sosial",
            "gamma-presentasi-profesional",
            "notebooklm-belajar-dari-dokumen",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("workshop", "0010_generalize_layout_variants"),
    ]

    operations = [
        migrations.RunPython(seed_new_workshops, remove_new_workshops),
    ]
