# Generated by Django 4.2.7 on 2024-10-07 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="image_url",
        ),
        migrations.AddField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
