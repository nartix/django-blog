# Generated by Django 5.0.2 on 2024-03-15 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_alter_blogpost_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='status',
        ),
    ]
