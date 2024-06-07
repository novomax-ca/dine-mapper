# Generated by Django 5.1 on 2024-06-05 22:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("map", "0005_rename_photo_marker_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="marker",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="photos/thumbnails/"
            ),
        ),
        migrations.AlterField(
            model_name="marker",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="photos/"),
        ),
    ]
