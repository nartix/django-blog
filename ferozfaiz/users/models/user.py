from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserAuthManager(UserManager):
    pass


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    username_editable = models.BooleanField(default=False)
    email2 = models.EmailField(blank=True, null=True)

    objects = CustomUserAuthManager()

    class Meta:
        db_table = "auth_user"
