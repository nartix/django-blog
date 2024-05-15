# Generated by Django 5.0.2 on 2024-03-05 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0002_alter_oauthprovider_authorization_base_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthuser',
            name='access_token',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='oauthuser',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
