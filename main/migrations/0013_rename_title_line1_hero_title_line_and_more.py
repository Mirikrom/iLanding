# Generated by Django 4.2.7 on 2024-12-11 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_rename_text_phone_number_about_phone_label"),
    ]

    operations = [
        migrations.RenameField(
            model_name="hero",
            old_name="title_line1",
            new_name="title_line",
        ),
        migrations.RemoveField(
            model_name="hero",
            name="title_line2",
        ),
        migrations.RemoveField(
            model_name="hero",
            name="title_line3",
        ),
    ]