from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model


class UserSetPasswordForm(SetPasswordForm):
    # Inherits from Django's SetPasswordForm which already has the
    # password and confirmation logic.

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UserSetPasswordForm, self).__init__(user=user, *args, **kwargs)
