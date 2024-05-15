from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from users.forms import EmailForm
from users.utils import UserAuthManager

User = get_user_model()


class ProfileEmailEditForm(EmailForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ProfileEmailEditForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Exclude the current user's email from the check
        if UserAuthManager.does_email_exist_exlude_self(self.user.pk, email):
            raise forms.ValidationError(
                _("Email already exists. Please use a different email.")
            )
        return email
