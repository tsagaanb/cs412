# Generated by Django 4.2.7 on 2024-10-17 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0008_statusmessage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]
