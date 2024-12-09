# Generated by Django 4.2.7 on 2024-11-27 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0003_alter_bookprogress_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="rating",
            field=models.IntegerField(
                blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True
            ),
        ),
    ]