from django.db import migrations, models


FULL_BIO = (
    "Kak Angga memiliki pengalaman lebih dari 10 tahun di bidang teknologi AI. "
    "Sebelumnya, ia berkarier sebagai AI Research Engineer di GRID Co., Ltd., "
    "dan saat ini aktif sebagai Research Assistant di National Institute of "
    "Advanced Industrial Science and Technology (AIST, 産業技術総合研究所), "
    "lembaga riset pemerintah Jepang yang berlokasi di Tokyo. "
    "Fokus dan minat risetnya saat ini meliputi Artificial Intelligence, "
    "Embodied AI, dan Human-Robot Interaction."
)


def populate_mentor_full_bio(apps, schema_editor):
    Mentor = apps.get_model("workshop", "Mentor")
    for mentor in Mentor.objects.filter(
        name__in=["Muhammad Angga Muttaqien", "Muhammad Angga Muttaqien, M.Eng."]
    ):
        fields = []
        if mentor.name != "Muhammad Angga Muttaqien, M.Eng.":
            mentor.name = "Muhammad Angga Muttaqien, M.Eng."
            fields.append("name")
        if not mentor.full_bio:
            mentor.full_bio = FULL_BIO
            fields.append("full_bio")
        if fields:
            mentor.save(update_fields=fields)


def reverse_mentor_full_bio(apps, schema_editor):
    Mentor = apps.get_model("workshop", "Mentor")
    Mentor.objects.filter(
        name="Muhammad Angga Muttaqien, M.Eng.",
    ).update(name="Muhammad Angga Muttaqien")


class Migration(migrations.Migration):

    dependencies = [
        ("workshop", "0011_seed_showcase_and_guide_workshops"),
    ]

    operations = [
        migrations.AddField(
            model_name="mentor",
            name="full_bio",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Profil lengkap mentor yang ditampilkan saat kartu mentor dibuka.",
            ),
        ),
        migrations.RunPython(populate_mentor_full_bio, reverse_mentor_full_bio),
    ]
