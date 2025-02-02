# Generated by Django 5.1.5 on 2025-02-02 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65)),
                ('slug', models.SlugField(blank=True, default=' ', max_length=255, unique=True)),
                ('is_published', models.BooleanField(default=False, help_text='Se marcado, página será exibida')),
                ('content', models.TextField()),
            ],
        ),
    ]
