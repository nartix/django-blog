# Generated by Django 5.0.2 on 2024-03-15 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_blogpost_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='status',
        ),
    ]
