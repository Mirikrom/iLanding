# Generated by Django 4.2.7 on 2024-12-12 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0016_basicpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="basicpage",
            name="menu_item",
            field=models.OneToOneField(
                blank=True,
                help_text="Bu sahifa qaysi menu elementi uchun",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="basic_page",
                to="main.menuitem",
                verbose_name="Menu elementi",
            ),
        ),
    ]