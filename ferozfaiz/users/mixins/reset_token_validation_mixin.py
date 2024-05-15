from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import logging


class ResetTokenValidationMixin:
    def dispatch(self, request, *args, **kwargs):
        token = kwargs["token"]
        user = self.get_user(kwargs["uidb64"])

        # PasswordResetConfirmView dispatch validates and sets token to 'set-password'
        # and redirects to password_reset_confirm with set-password as token
        if self.token_generator.check_token(user, token) or token == self.reset_url_token:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('users:password_reset_invalid')
