from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()


class PasswordResetUsernameEmailForm(forms.Form):
    username_or_email = forms.CharField(
        label=_("Username or Email"),
        min_length=3,
        max_length=254,  # Email max length + some extra buffer for usernames
        required=True,
    )

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get("username_or_email").strip()

        try:
            validate_email(username_or_email)
            self.cleaned_data["email"] = username_or_email
        except ValidationError:
            pass

        return username_or_email
