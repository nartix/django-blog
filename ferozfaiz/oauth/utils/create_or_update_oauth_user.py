from django.utils import timezone
from datetime import timedelta
from oauth.models import OAuthProvider, OAuthUser
import logging

logger = logging.getLogger("core")


def create_or_update_oauth_user(user, oauth_data):
    """
    Create or update an OAuthUser instance.

    Args:
        user (User): The Django user instance.
        oauth_data (dict): A dictionary containing OAuth user info and tokens.

    Returns:
        OAuthUser: The created or updated OAuthUser instance.
    """
    provider, _ = OAuthProvider.objects.get_or_create(
        name=oauth_data["provider"])
    expires_in_seconds = oauth_data.get("expires_in", 3600)
    expires_in = timezone.now() + timedelta(seconds=expires_in_seconds)

    oauth_data_copy = oauth_data.copy()
    oauth_data_copy.pop("access_token", None)
    oauth_data_copy.pop("refresh_token", None)

    logger.info(
        f"Creating or updating OAuthUser for {user.username} with provider {provider.name}")

    oauth_user, created = OAuthUser.objects.update_or_create(
        user=user,
        provider=provider,
        defaults={
            "uid": oauth_data["uid"],
            "email": oauth_data.get("email", ""),
            "access_token": oauth_data["access_token"],
            "refresh_token": oauth_data.get("refresh_token", ""),
            "expires_in": expires_in,
            # "profile_data": oauth_data.get("profile_data", {}),
            "profile_data": oauth_data_copy,
        },
    )
    return oauth_user
