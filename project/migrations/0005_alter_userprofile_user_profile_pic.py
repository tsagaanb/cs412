# Generated by Django 4.2.7 on 2024-12-06 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="user_profile_pic",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]