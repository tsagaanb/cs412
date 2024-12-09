# Generated by Django 4.2.7 on 2024-12-09 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0005_alter_userprofile_user_profile_pic"),
    ]

    operations = [
        migrations.CreateModel(
            name="FriendRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_requests",
                        to="project.userprofile",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_requests",
                        to="project.userprofile",
                    ),
                ),
            ],
        ),
    ]