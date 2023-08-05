# Generated by Django 4.0.3 on 2022-03-18 06:37

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0062_alter_addedstreamfieldwithemptylistdefaultpage_body_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="JSONBlockCountsStreamModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("text", wagtail.blocks.CharBlock()),
                            ("rich_text", wagtail.blocks.RichTextBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JSONMinMaxCountStreamModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("text", wagtail.blocks.CharBlock()),
                            ("rich_text", wagtail.blocks.RichTextBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JSONStreamModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("text", wagtail.blocks.CharBlock()),
                            ("rich_text", wagtail.blocks.RichTextBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
        ),
    ]
