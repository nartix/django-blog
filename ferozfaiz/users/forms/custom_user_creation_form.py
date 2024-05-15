from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from oauth.models import OAuthUser
from users.utils import UserAuthManager

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, min_length=4, max_length=254)
    username = forms.CharField(min_length=3, max_length=30, required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Check if the email already exists in the User or OAuthUser model
        if (UserAuthManager.does_email_exist(email)):
            raise ValidationError(
                _("Email already exists. Please use a different email.")
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")

        try:
            validate_email(username)
        except forms.ValidationError:
            # If it's not a valid email, return the username
            return username
        else:
            # If it's a valid email, raise an error
            raise ValidationError("Username cannot be an email address.")

    # defualt django form is already checking for username as case insensitive
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username__iexact=username).exists():
    #         raise ValidationError(
    #             _("A user with that username already exists."))
    #     return username
