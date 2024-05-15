# Generated by Django 5.0.2 on 2024-03-15 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_remove_blogpost_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.IntegerField(choices=[('draft', 'Draft'), ('published', 'Published')], default=0),
        ),
    ]