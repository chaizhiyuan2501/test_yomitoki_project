# Generated by Django 4.2.11 on 2025-04-13 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("guest", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="guest",
            old_name="full_name",
            new_name="name",
        ),
    ]
