# Generated by Django 5.0.2 on 2024-03-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_blogpost_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Published'), (2, 'Archived')], default=0),
        ),
    ]
