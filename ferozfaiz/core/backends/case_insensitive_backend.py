from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from users.utils import UserAuthManager


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = UserAuthManager.get_user_by_username_or_email(username)
        except User.DoesNotExist:
            return None

        if user and user.check_password(password):
            return user
