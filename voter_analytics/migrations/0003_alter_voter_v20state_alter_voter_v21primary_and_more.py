# Generated by Django 4.2.16 on 2024-11-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0002_alter_voter_address_apt_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="v20state",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v21primary",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v21town",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v22general",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="voter",
            name="v23town",
            field=models.BooleanField(default=False),
        ),
    ]
