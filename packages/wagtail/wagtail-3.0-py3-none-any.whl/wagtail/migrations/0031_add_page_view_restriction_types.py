# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 15:33
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0001_initial"),
        ("wagtailcore", "0030_index_on_pagerevision_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="pageviewrestriction",
            name="groups",
            field=models.ManyToManyField(blank=True, to="auth.Group"),
        ),
        migrations.AddField(
            model_name="pageviewrestriction",
            name="restriction_type",
            field=models.CharField(
                choices=[
                    ("none", "Public"),
                    ("login", "Private, accessible to logged-in users"),
                    ("password", "Private, accessible with the following password"),
                    ("groups", "Private, accessible to users in specific groups"),
                ],
                default="password",
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="pageviewrestriction",
            name="password",
            field=models.CharField(blank=True, max_length=255, verbose_name="password"),
        ),
    ]
