from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OAuthProvider(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client_id = models.CharField(max_length=255, null=True, blank=True)
    secret = models.CharField(max_length=255, null=True, blank=True)
    authorization_base_url = models.CharField(max_length=255, null=True, blank=True)
    token_url = models.CharField(max_length=255, null=True, blank=True)
    scope = models.CharField(max_length=255, null=True, blank=True)
    profile_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class OAuthUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="oauth_accounts"
    )
    provider = models.ForeignKey(OAuthProvider, on_delete=models.CASCADE)
    uid = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    access_token = models.CharField(max_length=2048)
    refresh_token = models.CharField(max_length=2048, blank=True, null=True)
    expires_in = models.DateTimeField(blank=True, null=True)
    profile_data = models.JSONField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.provider.name}"

    class Meta:
        unique_together = ("provider", "uid")
