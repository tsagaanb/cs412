# Generated by Django 4.2.7 on 2024-12-09 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0006_friendrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="friendrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
