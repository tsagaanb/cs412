# Generated by Django 4.2.7 on 2024-10-07 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0005_alter_profile_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
