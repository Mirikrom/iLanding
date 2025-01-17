# Generated by Django 4.2.7 on 2024-12-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_siteconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('feture_list', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('small_image', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('url', models.URLField(blank=True, null=True)),
                ('url_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
