from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from oauth.models import OAuthUser
from oauth.utils import create_or_update_oauth_user
from users.models import UnverifiedUser

User = get_user_model()


class UserAuthManager:
    @staticmethod
    def get_user_by_pk(pk):
        return User.objects.get(pk=pk)

    @staticmethod
    def get_oauth_user(email, provider_name):
        return OAuthUser.objects.filter(email__iexact=email, provider__name=provider_name).first()

    @staticmethod
    def get_user_by_email(email):
        return User.objects.get(email__iexact=email)

    @staticmethod
    def get_user_by_username(username):
        return User.objects.get(username__iexact=username)

    @staticmethod
    def does_username_exist(username):
        return User.objects.filter(username__iexact=username).exists()

    @staticmethod
    def create_or_update_oauth_user(user, oauth_user_info):
        return create_or_update_oauth_user(user, oauth_user_info)

    @staticmethod
    def does_email_exist(email):
        return User.objects.filter(email__iexact=email).exists() or OAuthUser.objects.filter(email__iexact=email).exists()

    @staticmethod
    def does_email_exist_exlude_self(pk, email):
        return User.objects.exclude(pk=pk).filter(email__iexact=email).exists()

    @staticmethod
    def do_email_pk_exist(pk, email):
        return User.objects.filter(email__iexact=email, pk=pk).exists() or OAuthUser.objects.filter(email__iexact=email, pk=pk).exists()

    @staticmethod
    @transaction.atomic
    def create_user_and_oauth_accounts(cleaned_data, oauth_user_info):
        user, created = User.objects.get_or_create(
            email=oauth_user_info["email"],
            defaults={
                "username": cleaned_data["username"],
                "first_name": oauth_user_info.get("first_name", ""),
                "last_name": oauth_user_info.get("last_name", ""),
            },
        )

        # Create or update OAuthUser
        UserAuthManager.create_or_update_oauth_user(user, oauth_user_info)
        return user

    @staticmethod
    def get_user_by_username_or_email(username):
        return User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

    @staticmethod
    def get_unverified_user_by_pk(pk):
        return UnverifiedUser.objects.get(pk=pk)

    @staticmethod
    def get_unverified_user_by_pk_email(pk, email):
        return UnverifiedUser.objects.filter(email__iexact=email, pk=pk).first()

    @staticmethod
    def get_user_by_pk_email2(pk, email2):
        return User.objects.get(email2__iexact=email2, pk=pk)

    @staticmethod
    def create_user(username, email, password, email_verified, username_editable):
        return User.objects.create(
            username=username,
            email=email,
            password=password,
            email_verified=email_verified,
            username_editable=username_editable,
        )

    @staticmethod
    @transaction.atomic
    def update_or_create_unverified_user(username, email, raw_password):
        return UnverifiedUser.objects.update_or_create(
            email__iexact=email,
            defaults={
                "email": email,
                "username": username,
                "password": make_password(raw_password),
            },
        )
