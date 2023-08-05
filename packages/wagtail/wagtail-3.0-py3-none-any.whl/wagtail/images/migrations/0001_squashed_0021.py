# Generated by Django 2.1.3 on 2018-11-20 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.models
import wagtail.images.models
import wagtail.search.index


# Functions from  wagtail.images.migrations.0002_initial_data


def add_image_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    Group = apps.get_model("auth.Group")

    # Get image permissions
    image_content_type, _created = ContentType.objects.get_or_create(
        model="image", app_label="wagtailimages"
    )

    add_image_permission, _created = Permission.objects.get_or_create(
        content_type=image_content_type,
        codename="add_image",
        defaults={"name": "Can add image"},
    )
    change_image_permission, _created = Permission.objects.get_or_create(
        content_type=image_content_type,
        codename="change_image",
        defaults={"name": "Can change image"},
    )
    delete_image_permission, _created = Permission.objects.get_or_create(
        content_type=image_content_type,
        codename="delete_image",
        defaults={"name": "Can delete image"},
    )

    # Assign it to Editors and Moderators groups
    for group in Group.objects.filter(name__in=["Editors", "Moderators"]):
        group.permissions.add(
            add_image_permission, change_image_permission, delete_image_permission
        )


def remove_image_permissions(apps, schema_editor):
    """Reverse the above additions of permissions."""
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    image_content_type = ContentType.objects.get(
        model="image",
        app_label="wagtailimages",
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=image_content_type,
        codename__in=("add_image", "change_image", "delete_image"),
    ).delete()


# Functions from  wagtail.images.migrations.0012_copy_image_permissions_to_collections


def get_image_permissions(apps):
    # return a queryset of the 'add_image' and 'change_image' permissions
    Permission = apps.get_model("auth.Permission")
    ContentType = apps.get_model("contenttypes.ContentType")

    image_content_type, _created = ContentType.objects.get_or_create(
        model="image",
        app_label="wagtailimages",
    )
    return Permission.objects.filter(
        content_type=image_content_type, codename__in=["add_image", "change_image"]
    )


def copy_image_permissions_to_collections(apps, schema_editor):
    Collection = apps.get_model("wagtailcore.Collection")
    Group = apps.get_model("auth.Group")
    GroupCollectionPermission = apps.get_model("wagtailcore.GroupCollectionPermission")

    root_collection = Collection.objects.get(depth=1)

    for permission in get_image_permissions(apps):
        for group in Group.objects.filter(permissions=permission):
            GroupCollectionPermission.objects.create(
                group=group, collection=root_collection, permission=permission
            )


def remove_image_permissions_from_collections(apps, schema_editor):
    GroupCollectionPermission = apps.get_model("wagtailcore.GroupCollectionPermission")
    image_permissions = get_image_permissions(apps)

    GroupCollectionPermission.objects.filter(permission__in=image_permissions).delete()


class Migration(migrations.Migration):

    replaces = [
        ("wagtailimages", "0001_initial"),
        ("wagtailimages", "0002_initial_data"),
        ("wagtailimages", "0003_fix_focal_point_fields"),
        ("wagtailimages", "0004_make_focal_point_key_not_nullable"),
        ("wagtailimages", "0005_make_filter_spec_unique"),
        ("wagtailimages", "0006_add_verbose_names"),
        ("wagtailimages", "0007_image_file_size"),
        ("wagtailimages", "0008_image_created_at_index"),
        ("wagtailimages", "0009_capitalizeverbose"),
        ("wagtailimages", "0010_change_on_delete_behaviour"),
        ("wagtailimages", "0011_image_collection"),
        ("wagtailimages", "0012_copy_image_permissions_to_collections"),
        ("wagtailimages", "0013_make_rendition_upload_callable"),
        ("wagtailimages", "0014_add_filter_spec_field"),
        ("wagtailimages", "0015_fill_filter_spec_field"),
        ("wagtailimages", "0016_deprecate_rendition_filter_relation"),
        ("wagtailimages", "0017_reduce_focal_point_key_max_length"),
        ("wagtailimages", "0018_remove_rendition_filter"),
        ("wagtailimages", "0019_delete_filter"),
        ("wagtailimages", "0020_add-verbose-name"),
        ("wagtailimages", "0021_image_file_hash"),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailcore", "0002_initial_data"),
        ("taggit", "0001_initial"),
        ("wagtailcore", "0026_group_collection_permission"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "file",
                    models.ImageField(
                        height_field="height",
                        upload_to=wagtail.images.models.get_upload_to,
                        verbose_name="file",
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(editable=False, verbose_name="width")),
                ("height", models.IntegerField(editable=False, verbose_name="height")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                ("focal_point_x", models.PositiveIntegerField(blank=True, null=True)),
                ("focal_point_y", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "focal_point_width",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "focal_point_height",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
                ("file_size", models.PositiveIntegerField(editable=False, null=True)),
                (
                    "collection",
                    models.ForeignKey(
                        default=wagtail.models.get_root_collection_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.Collection",
                        verbose_name="collection",
                    ),
                ),
                (
                    "file_hash",
                    models.CharField(blank=True, editable=False, max_length=40),
                ),
            ],
            options={
                "abstract": False,
                "verbose_name": "image",
                "verbose_name_plural": "images",
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name="Rendition",
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
                    "file",
                    models.ImageField(
                        height_field="height",
                        upload_to=wagtail.images.models.get_rendition_upload_to,
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(editable=False)),
                ("height", models.IntegerField(editable=False)),
                (
                    "focal_point_key",
                    models.CharField(
                        blank=True, default="", editable=False, max_length=16
                    ),
                ),
                ("filter_spec", models.CharField(db_index=True, max_length=255)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="renditions",
                        to="wagtailimages.Image",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="rendition",
            unique_together={("image", "filter_spec", "focal_point_key")},
        ),
        migrations.RunPython(
            add_image_permissions_to_admin_groups, remove_image_permissions
        ),
        migrations.RunPython(
            copy_image_permissions_to_collections,
            remove_image_permissions_from_collections,
        ),
    ]
