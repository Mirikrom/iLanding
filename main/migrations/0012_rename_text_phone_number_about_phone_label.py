# Generated by Django 4.2.7 on 2024-12-11 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_about_text_phone_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="about",
            old_name="text_phone_number",
            new_name="phone_label",
        ),
    ]
