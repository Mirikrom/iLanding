# Generated by Django 4.2.7 on 2024-12-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='avatars/')),
                ('alt_text', models.CharField(max_length=100)),
                ('sort_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_text', models.CharField(max_length=255)),
                ('title_line1', models.CharField(max_length=255)),
                ('title_line2', models.CharField(max_length=255)),
                ('title_line3', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_button_text', models.CharField(max_length=100)),
                ('start_button_url', models.CharField(max_length=255)),
                ('video_button_text', models.CharField(max_length=100)),
                ('video_button_url', models.CharField(max_length=255)),
                ('hero_image', models.ImageField(upload_to='hero/')),
                ('customers_text', models.CharField(max_length=255)),
                ('additional_customers_count', models.IntegerField(default=0)),
                ('customer_avatars', models.ManyToManyField(to='main.customeravatar')),
            ],
            options={
                'verbose_name': 'Hero Section',
                'verbose_name_plural': 'Hero Section',
            },
        ),
    ]