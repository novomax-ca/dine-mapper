# Generated by Django 5.1 on 2024-06-05 22:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("map", "0004_marker_photo_alter_marker_latitude_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="marker",
            old_name="photo",
            new_name="image",
        ),
    ]
