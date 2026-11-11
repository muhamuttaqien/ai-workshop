from django.db import migrations, models


DURATION_LABEL = "2 Hari • Total 3 Jam (Live) + 6 Jam (Online)"


def standardize_pricing_and_duration(apps, schema_editor):
    Workshop = apps.get_model("workshop", "Workshop")

    Workshop.objects.all().update(
        original_price_label="Rp780.000",
        price_label="Rp390.000",
        discount_label="50% OFF",
        duration_label=DURATION_LABEL,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0006_perplexity_workshop_and_standardize_format"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workshop",
            name="duration_label",
            field=models.CharField(
                default=DURATION_LABEL,
                max_length=120,
            ),
        ),
        migrations.AddField(
            model_name="workshop",
            name="original_price_label",
            field=models.CharField(default="Rp780.000", max_length=80),
        ),
        migrations.AlterField(
            model_name="workshop",
            name="price_label",
            field=models.CharField(default="Rp390.000", max_length=80),
        ),
        migrations.AddField(
            model_name="workshop",
            name="discount_label",
            field=models.CharField(default="50% OFF", max_length=40),
        ),
        migrations.RunPython(standardize_pricing_and_duration, migrations.RunPython.noop),
    ]
