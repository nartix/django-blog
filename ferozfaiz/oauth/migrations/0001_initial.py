# Generated by Django 5.0.2 on 2024-03-05 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('client_id', models.CharField(max_length=255)),
                ('secret', models.CharField(max_length=255)),
                ('authorization_base_url', models.CharField(max_length=255)),
                ('token_url', models.CharField(max_length=255)),
                ('scope', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OAuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('access_token', models.CharField(max_length=1024)),
                ('refresh_token', models.CharField(blank=True, max_length=1024, null=True)),
                ('expires_in', models.DateTimeField(blank=True, null=True)),
                ('profile_data', models.JSONField(blank=True, null=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth.oauthprovider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oauth_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('provider', 'uid')},
            },
        ),
    ]
