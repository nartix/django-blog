from django.db import models
from django.utils import timezone


class UnverifiedUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.email

    def token_is_expired(self):
        # Check if more than 2 days have passed since the timestamp
        return timezone.now() - self.created_at > timezone.timedelta(days=2)

    class Meta:
        db_table = "auth_user_unverified"
