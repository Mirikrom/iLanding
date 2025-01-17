# Generated by Django 4.2.7 on 2024-12-12 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0018_alter_basicpage_menu_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basicpage",
            name="menu_item",
            field=models.OneToOneField(
                blank=True,
                help_text="Bu sahifa qaysi menu elementi uchun",
                limit_choices_to={
                    "basic_page__isnull": True,
                    "url__startswith": "/basic/",
                },
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="basic_page",
                to="main.menuitem",
                verbose_name="Menu elementi",
            ),
        ),
    ]
