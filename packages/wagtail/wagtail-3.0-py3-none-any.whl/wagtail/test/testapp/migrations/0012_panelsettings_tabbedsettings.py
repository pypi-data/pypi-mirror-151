# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 09:58
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0011_userprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="PanelSettings",
            fields=[
                (
                    "testsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tests.TestSetting",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("tests.testsetting",),
        ),
        migrations.CreateModel(
            name="TabbedSettings",
            fields=[
                (
                    "testsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tests.TestSetting",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("tests.testsetting",),
        ),
    ]
