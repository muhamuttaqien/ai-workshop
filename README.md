# Indonesia AI Workshop — Django

Website dinamis untuk program **AI Workshop Indonesia AI**. Project ini dibangun dengan Django agar workshop baru dapat ditambahkan, diduplikasi, diarsipkan, dan dikelola melalui Django Admin tanpa membuat halaman HTML baru untuk setiap event.

Saat ini seluruh workshop menggunakan format **Zoom Online**, harga promo **Rp390.000** dari harga normal **Rp780.000 (50% OFF)**, durasi **2 Hari • Total 3 Jam (Live) + 6 Jam (Online)**, mentor yang dapat dipakai ulang antar-workshop, testimonial global, CTA pendaftaran untuk workshop aktif, dan CTA **Request Beli Rekaman** untuk workshop yang sudah selesai.

---

## 1. Fitur utama

- Halaman utama `/` otomatis menampilkan workshop published yang paling dekat dan belum selesai.
- Detail workshop dibuat dinamis dari database melalui satu template utama.
- Workshop lama tetap memiliki halaman detail dan CTA **Request Beli Rekaman**.
- Pada halaman workshop lama, tombol **Lihat workshop terbaru** selalu menuju workshop published dengan `start_date` paling baru di database, bukan sekadar event berikutnya secara kronologis.
- Halaman `/workshops/` menampilkan seluruh workshop published.
- Django Admin mendukung pembuatan workshop baru tanpa mengedit JSON.
- Workshop dapat diduplikasi dari Admin sebagai draft.
- Tiga variasi layout tersedia:
  - `research` — gaya terbaru / Claude-style.
  - `productivity` — gaya ChatGPT productivity.
  - `reporting` — gaya Gemini reporting.
- Mentor dapat dipakai ulang pada banyak workshop.
- Testimonial bersifat global dan ditampilkan sebagai slider.
- Konten workshop disimpan sebagai model relational: audience, curriculum, benefits, schedule, FAQ, dan lain-lain.
- Font Awesome dipakai untuk icon navigasi, CTA, jadwal, slider, dan elemen UI terkait.
- Responsive untuk desktop, tablet, dan mobile.

---

## 2. Workshop yang tersedia

Urutan berikut dari **paling lama sampai paling baru** berdasarkan `start_date`.

| No. | Tanggal | Workshop | Tool | Use case | Layout | Format | Harga | Status |
|---:|---|---|---|---|---|---|---|---|
| 1 | 3 & 4 September 2026 | Pakai Perplexity untuk Riset Pasar & Kompetitor | Perplexity | Market & competitor research | Research | Zoom Online | Rp390.000 | Selesai |
| 2 | 17 & 18 September 2026 | Pakai Gemini untuk Membuat Laporan Kerja | Gemini | Work reporting | Reporting | Zoom Online | Rp390.000 | Selesai |
| 3 | 1 & 2 Oktober 2026 | Pakai ChatGPT untuk Pendataan Harian | ChatGPT | Daily data logging | Productivity | Zoom Online | Rp390.000 | Selesai |
| 4 | 15 & 16 Oktober 2026 | Belajar Claude untuk Riset | Claude | Master & doctoral research | Research | Zoom Online | Rp390.000 | Terbaru / mendatang |

URL seed workshop:

```text
/workshop/perplexity-riset-pasar-kompetitor/
/workshop/gemini-laporan-kerja/
/workshop/chatgpt-pendataan-harian/
/workshop/claude-untuk-riset/
```

> Catatan: urutan terbaru pada website **tidak di-hard-code** dari daftar README ini. Website mengambil data workshop published langsung dari database.

---

## 3. Struktur URL

```text
/                         Homepage, workshop aktif/terdekat
/workshops/               Daftar seluruh workshop published
/workshop/<slug>/         Detail workshop
/admin/                   Django Admin
```

Contoh:

```text
http://127.0.0.1:8000/workshop/claude-untuk-riset/
```

---

## 4. Struktur project

```text
ai-workshop-django/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── workshop/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   ├── 0001_initial.py
    │   ├── 0002_seed_workshops.py
    │   ├── 0003_admin_friendly_content.py
    │   ├── 0004_workshop_history_updates.py
    │   ├── 0005_reporting_layout_variant.py
    │   └── 0006_perplexity_workshop_and_standardize_format.py
    ├── templates/workshop/
    │   ├── base.html
    │   ├── detail.html
    │   ├── list.html
    │   └── includes/
    │       ├── header.html
    │       ├── footer.html
    │       └── mobile_cta.html
    └── static/workshop/
        ├── style.css
        ├── script.js
        └── img/
```

`base.html` adalah layout global. Header dan footer dipisahkan sebagai reusable partial. `detail.html` dipakai untuk semua workshop dan memilih variasi visual berdasarkan `layout_variant`.

---

## 5. Persyaratan

- Python 3.11+ direkomendasikan.
- Django 5.2.x.
- SQLite dipakai sebagai database development default.

Install dependency dari:

```text
requirements.txt
```

---

## 6. Menjalankan project pertama kali

Buat virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan migration:

```bash
python manage.py migrate
```

Buat akun admin:

```bash
python manage.py createsuperuser
```

Jalankan development server:

```bash
python manage.py runserver
```

Buka:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

---

## 7. Environment variables

`config/settings.py` membaca environment variable berikut:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
WORKSHOP_REGISTRATION_URL
WORKSHOP_RECORDING_REQUEST_URL
```

Contoh ada di `.env.example`:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.1.10
WORKSHOP_REGISTRATION_URL=https://example.com/daftar
WORKSHOP_RECORDING_REQUEST_URL=https://example.com/request-rekaman
```

Project ini menggunakan `os.getenv()` langsung. File `.env.example` adalah referensi konfigurasi; jika ingin file `.env` dibaca otomatis, tambahkan loader environment sesuai deployment yang digunakan, atau export variable dari shell/server.

Contoh Linux/macOS:

```bash
export WORKSHOP_REGISTRATION_URL="https://example.com/daftar"
export WORKSHOP_RECORDING_REQUEST_URL="https://example.com/request-rekaman"
```

---

## 8. Masuk ke Django Admin

Pastikan sudah membuat superuser:

```bash
python manage.py createsuperuser
```

Kemudian buka:

```text
http://127.0.0.1:8000/admin/
```

Di Admin tersedia:

- **Workshops**
- **Mentors**
- **Testimonials**

Workshop adalah pusat data utama. Audience, materi, benefit, jadwal, dan FAQ ditambahkan sebagai inline di halaman Workshop.

---

## 9. Membuat workshop baru

Buka:

```text
Admin → Workshops → Add workshop
```

Isi minimal:

1. Judul workshop.
2. Slug.
3. Headline dan headline accent.
4. Deskripsi.
5. Tanggal mulai dan selesai.
6. Label tanggal dan hari.
7. Jam.
8. Mentor.
9. Judul section.
10. Intro, audience, curriculum, benefit, schedule, dan FAQ melalui inline.

Default `format_label` untuk workshop baru adalah:

```text
Zoom Online
```

Harga seed workshop saat ini adalah:

```text
Rp390.000
```

Untuk halaman dengan tampilan terbaru, gunakan:

```text
Layout variant: Latest / Research (Claude-style)
```

Workshop baru sebaiknya dibuat sebagai draft lebih dulu:

```text
Published = False
```

Setelah konten selesai dicek:

```text
Published = True
```

---

## 10. Duplicate workshop

Jika struktur workshop baru mirip workshop yang sudah ada, gunakan fungsi duplicate agar lebih cepat.

Di halaman daftar Workshop pada Django Admin:

1. Centang workshop sumber.
2. Pilih action **Duplicate workshop terpilih sebagai draft**.
3. Klik **Go**.
4. Buka workshop hasil copy.
5. Ubah judul, slug, tanggal, materi, harga, dan konten lain.
6. Aktifkan `Published` setelah selesai.

Workshop hasil duplicate otomatis:

- `Published = False`
- `Show registration = False`
- `Archived = False`
- URL pendaftaran dikosongkan.

Konten anak yang ikut disalin:

- Intro paragraphs
- Outcomes
- Audience
- Curriculum modules
- Benefits
- Schedule
- FAQ

---

## 11. Status workshop: aktif, selesai, dan arsip

Property `Workshop.has_ended` bernilai benar jika:

- `is_archived=True`, atau
- `end_date` sudah lebih kecil daripada tanggal hari ini.

Workshop selesai menggunakan CTA:

```text
Request Beli Rekaman
```

URL CTA menggunakan:

```text
WORKSHOP_RECORDING_REQUEST_URL
```

Jika variable itu kosong, sistem fallback ke `WORKSHOP_REGISTRATION_URL`.

Workshop aktif menggunakan CTA pendaftaran apabila:

```text
show_registration=True
```

---

## 12. Logika workshop terbaru

Ada dua konsep yang berbeda:

### Homepage `/`

Homepage memilih workshop published yang:

1. Belum diarsipkan.
2. Belum selesai.
3. Punya tanggal mulai paling dekat.

Jika tidak ada workshop mendatang, homepage menampilkan workshop published dengan `start_date` paling baru.

### Tombol “Lihat workshop terbaru” pada workshop lama

Tombol ini **selalu** mencari workshop published dengan:

```text
start_date paling besar
```

Jadi contoh dengan data saat ini:

```text
Perplexity 3–4 Sep
Gemini 17–18 Sep
ChatGPT 1–2 Okt
Claude 15–16 Okt
```

Jika membuka halaman Perplexity, Gemini, atau ChatGPT dan menekan **Lihat workshop terbaru**, tujuan adalah:

```text
Belajar Claude untuk Riset — 15 & 16 Oktober 2026
```

Bukan sekadar workshop berikutnya setelah event yang sedang dibuka.

---

## 13. Format dan harga standar

Migration `0006_perplexity_workshop_and_standardize_format.py` menstandardisasi workshop yang sudah ada menjadi:

```text
Format: Zoom Online
Harga normal : Rp780.000
Harga promo  : Rp390.000 (50% OFF)
```

Default model untuk workshop baru juga:

```text
Zoom Online
```

---

## 14. Bonus modul tools AI

Benefit **Belasan Modul Tools AI** pada data workshop menggunakan deskripsi standar:

> Belasan modul tambahan tentang tools AI seperti ChatGPT, Claude, Gemini, Perplexity dan lainnya.

Migration `0006` memperbarui benefit dengan visual `modules` pada workshop yang sudah ada agar copy-nya konsisten.

---

## 15. Model data

### `Workshop`

Menyimpan identitas utama workshop, jadwal, status, layout, harga, hero, mentor, dan heading section.

### `Mentor`

Mentor terpisah agar satu mentor bisa digunakan oleh banyak workshop.

### `Testimonial`

Testimonial global dan dapat digunakan lintas workshop.

### Model konten terkait

- `WorkshopIntroParagraph`
- `WorkshopOutcome`
- `WorkshopAudience`
- `WorkshopCurriculumModule`
- `WorkshopBenefit`
- `WorkshopScheduleItem`
- `WorkshopFAQ`

Konten tidak lagi disimpan sebagai JSON mentah sehingga lebih nyaman dikelola dari Admin.

---

## 16. Curriculum dan Session Key

Setiap modul curriculum mempunyai `session_key`.

Modul yang berada dalam sesi yang sama harus memakai `session_key` yang sama, misalnya:

```text
day-01
day-01
day-01
day-02
day-02
day-02
```

Untuk setiap modul isi pula:

- Session label
- Session title
- Session day
- Session time
- Number
- Title
- Text
- Sort order

Template mengelompokkan modul berdasarkan `session_key` melalui logic di `views.py`.

---

## 17. Layout variant

### Research

```text
research
```

Gaya halaman terbaru yang pertama kali digunakan pada **Belajar Claude untuk Riset**. Cocok untuk workshop riset, pembelajaran, knowledge work, dan use case yang membutuhkan penjelasan lebih mendalam.

### Productivity

```text
productivity
```

Gaya alternatif untuk workflow kerja dan productivity use case. Dipakai oleh workshop ChatGPT Pendataan Harian.

### Reporting

```text
reporting
```

Gaya ketiga yang berbeda secara visual, dengan elemen dashboard/report. Dipakai oleh workshop Gemini Laporan Kerja.

Jika belum ada kebutuhan desain khusus, gunakan `research` untuk workshop baru.

---

## 18. Mengakses dari laptop lain pada Wi-Fi yang sama

Cari IP laptop server:

```bash
hostname -I
```

Contoh:

```text
192.168.1.10
```

Set allowed hosts:

```bash
export DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost,192.168.1.10"
```

Jalankan Django pada seluruh interface:

```bash
python manage.py runserver 0.0.0.0:8000
```

Dari laptop lain pada jaringan yang sama buka:

```text
http://192.168.1.10:8000/
```

Admin:

```text
http://192.168.1.10:8000/admin/
```

Jika tidak bisa diakses, cek firewall dan pastikan router tidak mengaktifkan AP/Client Isolation.

Ubuntu dengan UFW:

```bash
sudo ufw allow 8000/tcp
```

---

## 19. Static files

Static asset berada di:

```text
workshop/static/workshop/
```

Template memanggil asset dengan Django `{% static %}`.

Untuk production jalankan:

```bash
python manage.py collectstatic
```

`STATIC_ROOT` adalah:

```text
staticfiles/
```

---

## 20. Testing

Jalankan test suite:

```bash
python manage.py test
```

Test mencakup antara lain:

- Dynamic detail route.
- Homepage memilih workshop aktif.
- Related content dirender dari database.
- Draft tidak dapat diakses publik.
- Workshop list.
- Layout reporting.
- CTA request rekaman.
- Default format Zoom Online.
- Halaman workshop lama mengarahkan **Lihat workshop terbaru** ke workshop published paling baru.

---

## 21. Migration history

### `0001_initial.py`

Schema awal project.

### `0002_seed_workshops.py`

Seed workshop awal Claude dan ChatGPT.

### `0003_admin_friendly_content.py`

Mengubah struktur konten dari JSON menjadi model relational yang lebih mudah dikelola melalui Admin.

### `0004_workshop_history_updates.py`

- Koreksi ChatGPT menjadi 1 & 2 Oktober 2026.
- Standardisasi harga menjadi Rp780.000 → Rp390.000 (50% OFF).
- Menambahkan workshop Gemini 17 & 18 September 2026.
- Menambahkan behavior arsip dan request rekaman.

### `0005_reporting_layout_variant.py`

Menambahkan layout `reporting` dan menerapkannya pada workshop Gemini.

### `0006_perplexity_workshop_and_standardize_format.py`

- Menambahkan workshop Perplexity 3 & 4 September 2026.
- Mengubah seluruh workshop menjadi **Zoom Online**.
- Memastikan harga workshop Rp390.000 dengan harga normal Rp780.000 dan label 50% OFF.
- Menstandardisasi deskripsi benefit Belasan Modul Tools AI.
- Mengubah default `format_label` workshop baru menjadi Zoom Online.

Setelah menerima update repo, jalankan:

```bash
python manage.py migrate
```

---

## 22. Catatan deployment production

Development server Django:

```bash
python manage.py runserver
```

hanya untuk development/testing.

Untuk production:

- Gunakan secret key yang kuat.
- Set `DJANGO_DEBUG=False`.
- Atur `DJANGO_ALLOWED_HOSTS` ke domain production.
- Jalankan `collectstatic`.
- Gunakan WSGI/ASGI server yang sesuai dengan infrastruktur deployment.
- Gunakan HTTPS pada reverse proxy/web server.
- Backup database sebelum migration besar.

---

# 23. 100 ide workshop ke depan — Tool × Use Case

Daftar ini adalah **ide editorial**, bukan event yang sudah dijadwalkan. Tool dan use case dapat disesuaikan dengan kebutuhan audiens Indonesia AI.

## A. ChatGPT — Productivity & Business

1. **ChatGPT × Menulis Email Profesional** — menyusun, merapikan, dan menyesuaikan tone email kerja.
2. **ChatGPT × Membuat SOP** — mengubah proses kerja menjadi SOP yang lebih terstruktur.
3. **ChatGPT × Customer Service** — membangun template respons dan knowledge workflow layanan pelanggan.
4. **ChatGPT × Sales Follow-up** — menyusun pesan follow-up berdasarkan konteks prospek.
5. **ChatGPT × Meeting Notes** — mengubah catatan rapat menjadi summary, decision, dan action items.
6. **ChatGPT × Job Description** — membantu HR menyusun deskripsi pekerjaan dan kriteria kandidat.
7. **ChatGPT × Proposal Bisnis** — membangun struktur proposal dari brief awal.
8. **ChatGPT × Content Calendar** — menyusun ide dan kalender konten bulanan.
9. **ChatGPT × Analisis Feedback Pelanggan** — mengelompokkan komentar menjadi tema dan insight.
10. **ChatGPT × Training Internal** — membuat outline modul dan materi pelatihan perusahaan.

## B. Claude — Research, Writing & Knowledge Work

11. **Claude × Literature Review** — membaca dan membandingkan paper akademik.
12. **Claude × Thesis Planning** — mengembangkan research question dan struktur tesis.
13. **Claude × Critical Reading** — membedah argumen, asumsi, dan keterbatasan dokumen panjang.
14. **Claude × Academic Writing** — mengecek struktur argumen dan coherence tulisan.
15. **Claude × Policy Document Analysis** — meringkas dan membandingkan dokumen kebijakan panjang.
16. **Claude × Research Interview Analysis** — mengelompokkan tema dari transkrip wawancara.
17. **Claude × Knowledge Synthesis** — menggabungkan insight dari beberapa dokumen menjadi satu brief.
18. **Claude × Book Chapter Development** — mengembangkan outline dan alur bab dari catatan penulis.
19. **Claude × Peer Review Simulation** — meminta critique terstruktur terhadap draft artikel.
20. **Claude × Technical Documentation** — merapikan dokumentasi teknis dari catatan engineering.

## C. Gemini — Google Workspace & Reporting

21. **Gemini × Laporan Kerja Mingguan** — mengubah catatan aktivitas menjadi laporan terstruktur.
22. **Gemini × Google Sheets Analysis** — membantu membaca pola dan menyusun pertanyaan analisis data kerja.
23. **Gemini × Presentasi Internal** — mengubah brief menjadi struktur presentasi yang jelas.
24. **Gemini × Project Update** — menyusun update progres, issue, dan next action.
25. **Gemini × Marketing Report** — membantu merangkum hasil campaign dan poin evaluasi.
26. **Gemini × HR Monthly Report** — menyusun ringkasan aktivitas dan indikator HR.
27. **Gemini × Meeting Preparation** — membuat agenda, background brief, dan pertanyaan diskusi.
28. **Gemini × Product Documentation** — membantu merapikan requirement dan catatan produk.
29. **Gemini × Executive Summary** — memadatkan laporan panjang menjadi ringkasan untuk manajemen.
30. **Gemini × Personal Productivity** — membangun workflow AI untuk pekerjaan administratif harian.

## D. Perplexity — Search & External Research

31. **Perplexity × Market Research** — memetakan pasar dan sumber informasi eksternal.
32. **Perplexity × Competitor Research** — membandingkan positioning dan informasi kompetitor.
33. **Perplexity × Industry Trend Scanning** — mencari perkembangan terbaru dalam suatu industri.
34. **Perplexity × Vendor Research** — membuat shortlist awal vendor berdasarkan kebutuhan.
35. **Perplexity × Travel Research** — menyusun riset destinasi, transportasi, dan aktivitas dari berbagai sumber.
36. **Perplexity × Product Benchmarking** — membandingkan produk berdasarkan kriteria yang ditentukan.
37. **Perplexity × Source Verification Workflow** — belajar menelusuri klaim kembali ke sumber asli.
38. **Perplexity × Business Idea Validation** — mengeksplorasi demand, pemain, dan asumsi pasar awal.
39. **Perplexity × Technology Landscape** — memetakan tool, perusahaan, dan pendekatan dalam kategori teknologi.
40. **Perplexity × News Research** — menyusun background sebuah isu dari beberapa sumber.

## E. NotebookLM — Learning & Knowledge Base

41. **NotebookLM × Belajar dari PDF** — membangun workflow belajar dari kumpulan dokumen.
42. **NotebookLM × Persiapan Ujian** — membuat pertanyaan belajar dari materi sendiri.
43. **NotebookLM × Company Knowledge Base** — memanfaatkan dokumen internal sebagai sumber tanya jawab.
44. **NotebookLM × Onboarding Karyawan** — menyusun materi onboarding berbasis dokumen perusahaan.
45. **NotebookLM × Research Notes** — mengorganisasi sumber dan catatan penelitian.
46. **NotebookLM × Book Discussion** — membandingkan konsep dari beberapa buku atau chapter.
47. **NotebookLM × Training Material Review** — membantu peserta menavigasi materi pelatihan panjang.
48. **NotebookLM × Project Documentation** — membangun workspace tanya jawab untuk dokumentasi proyek.
49. **NotebookLM × Course Companion** — membuat pendamping belajar berbasis slide dan handout kelas.
50. **NotebookLM × Interview Preparation** — belajar dari dokumen perusahaan, role, dan bahan yang disediakan sendiri.

## F. Canva AI — Design & Content Production

51. **Canva AI × Social Media Design** — membuat workflow desain konten rutin.
52. **Canva AI × Presentasi Bisnis** — menyusun visual presentasi dari brief.
53. **Canva AI × Poster Event** — membangun beberapa variasi poster dengan konsistensi brand.
54. **Canva AI × Marketing Kit** — menyiapkan aset campaign lintas format.
55. **Canva AI × Infografis** — mengubah informasi kompleks menjadi visual yang lebih ringkas.
56. **Canva AI × Recruitment Content** — membuat materi employer branding dan lowongan.
57. **Canva AI × Education Content** — membuat worksheet, slide, dan materi visual kelas.
58. **Canva AI × UMKM Branding** — membuat aset visual dasar untuk bisnis kecil.
59. **Canva AI × Event Documentation** — mengubah dokumentasi acara menjadi recap content.
60. **Canva AI × Personal Branding** — membangun template konten profesional yang konsisten.

## G. Gamma — Presentation & Communication

61. **Gamma × Pitch Deck** — menyusun narasi dan struktur deck bisnis.
62. **Gamma × Research Presentation** — mengubah hasil riset menjadi presentasi yang terstruktur.
63. **Gamma × Sales Deck** — membuat deck penjualan berbasis kebutuhan pelanggan.
64. **Gamma × Training Deck** — mengubah outline pelatihan menjadi presentasi.
65. **Gamma × Company Profile** — membangun company profile dari brief dan bahan internal.
66. **Gamma × Project Proposal** — membuat deck proposal proyek dari scope awal.
67. **Gamma × Workshop Material** — membuat materi workshop yang modular.
68. **Gamma × Portfolio Presentation** — menyusun karya menjadi narasi portfolio.
69. **Gamma × Quarterly Review** — membuat deck review kinerja periode tertentu.
70. **Gamma × Product Launch** — menyusun presentasi launch dari positioning dan key messages.

## H. n8n / Make / Zapier — Automation

71. **n8n × Lead Intake Automation** — mengalirkan data lead dari form ke workflow internal.
72. **n8n × AI Email Triage** — mengelompokkan email dan menyiapkan draft tindakan.
73. **n8n × Content Pipeline** — menghubungkan idea intake, drafting, review, dan publishing queue.
74. **n8n × Customer Feedback Pipeline** — mengumpulkan feedback dan mengelompokkannya otomatis.
75. **Make × Social Media Workflow** — menghubungkan data konten dengan proses produksi rutin.
76. **Make × Report Automation** — menggabungkan data dan menghasilkan draft report berkala.
77. **Zapier × Form to CRM** — mengotomasi aliran data dari form ke CRM dan notifikasi tim.
78. **Zapier × Meeting Follow-up** — membuat action item dan follow-up setelah meeting.
79. **n8n × AI Knowledge Workflow** — menghubungkan sumber dokumen dengan proses summary dan routing.
80. **Make × Admin Operations** — mengotomasi tugas administrasi repetitif lintas aplikasi.

## I. Cursor / GitHub Copilot — Coding & Software Work

81. **Cursor × Membuat Landing Page** — membangun halaman web dari requirement hingga refinement.
82. **Cursor × Debugging Python** — menggunakan AI untuk membaca error dan memperbaiki kode secara sistematis.
83. **Cursor × Django Development** — membuat model, view, template, dan admin dengan bantuan AI.
84. **Cursor × Refactoring Code** — memperbaiki struktur kode tanpa mengubah behavior utama.
85. **GitHub Copilot × Unit Testing** — membantu menyusun test case dari behavior aplikasi.
86. **GitHub Copilot × API Integration** — mempercepat boilerplate integrasi API.
87. **Cursor × Codebase Navigation** — memahami repository yang belum familiar.
88. **Cursor × Documentation** — menghasilkan dan memperbarui dokumentasi dari codebase.
89. **GitHub Copilot × SQL Queries** — membantu menyusun query dan menjelaskan logic data.
90. **Cursor × Data Processing Script** — membuat utility script untuk CSV, JSON, dan pekerjaan data rutin.

## J. Generative Visual & Video AI

91. **Adobe Firefly × Marketing Visual** — membuat dan memodifikasi visual campaign.
92. **Adobe Firefly × Product Mockup** — mengeksplorasi variasi tampilan produk dan background.
93. **Midjourney × Visual Concepting** — membuat moodboard dan arah visual awal.
94. **Midjourney × Storyboard** — mengeksplorasi frame visual sebelum produksi konten.
95. **Runway × Short Video Content** — membangun workflow ide ke video pendek.
96. **Runway × B-roll Generation** — membuat materi pendukung untuk video presentasi atau sosial media.
97. **Generative AI × Thumbnail Design** — mengeksplorasi konsep thumbnail yang lebih cepat.
98. **Generative AI × Infographic Illustration** — membuat aset ilustratif untuk penjelasan konsep.
99. **Generative AI × Product Campaign Concept** — menghasilkan variasi creative direction sebelum desain final.
100. **Generative AI × Educational Visuals** — membuat ilustrasi pendukung untuk materi belajar dan workshop.

---

## 24. Prinsip memilih workshop berikutnya

Daftar 100 ide di atas sebaiknya tidak diperlakukan sebagai urutan prioritas otomatis. Pemilihan workshop dapat mempertimbangkan:

- Masalah nyata yang sering dialami audiens.
- Tool yang sudah cukup stabil untuk dipakai dalam workshop hands-on.
- Use case yang dapat selesai dipraktikkan dalam dua sesi.
- Output konkret yang bisa dibawa pulang peserta.
- Tingkat overlap dengan workshop yang sudah pernah dilakukan.
- Ketersediaan mentor dan contoh kasus.
- Kemudahan peserta mengikuti tanpa setup teknis berlebihan.

Format positioning yang konsisten dapat dibuat sebagai:

```text
Pakai [TOOL] untuk [USE CASE]
```

atau untuk topik yang lebih edukatif:

```text
Belajar [TOOL/KONSEP] untuk [AUDIENS/KEBUTUHAN]
```

Contoh:

```text
Pakai Perplexity untuk Riset Kompetitor
Pakai Gemini untuk Membuat Laporan Kerja
Pakai ChatGPT untuk Pendataan Harian
Belajar Claude untuk Riset
```

---

## 25. Checklist sebelum publish workshop baru

- [ ] Judul dan slug sudah benar.
- [ ] Tanggal mulai dan selesai sudah benar.
- [ ] `dates_label` sesuai tanggal database.
- [ ] Jam sudah benar.
- [ ] Format tertulis `Zoom Online`.
- [ ] Harga sudah diperiksa.
- [ ] Mentor sudah dipilih.
- [ ] Intro sudah terisi.
- [ ] Audience sudah terisi.
- [ ] Curriculum dan session key sudah benar.
- [ ] Benefit sudah terisi.
- [ ] Benefit modul AI menggunakan copy yang sesuai.
- [ ] Schedule sudah terisi.
- [ ] FAQ sudah terisi.
- [ ] Link pendaftaran sudah benar.
- [ ] Layout variant sudah dipilih.
- [ ] Halaman sudah dicek desktop dan mobile.
- [ ] Workshop masih draft sebelum review selesai.
- [ ] `Published=True` hanya setelah final review.



### FAQ perangkat

Untuk seluruh workshop, spesifikasi laptop tidak perlu khusus. Peserta cukup menggunakan **laptop standar yang biasa digunakan untuk aktivitas sehari-hari**.
