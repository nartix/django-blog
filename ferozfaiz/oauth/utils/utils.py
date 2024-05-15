from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from core.utils import redirect_with_message

import logging

logger = logging.getLogger("core")

User = get_user_model()


def handle_oauth_user_found(request, oauth_user, user_info, next_url, UserAuthManager):
    # Existing OAuthUser found, check if the user is already logged in
    if request.user.is_authenticated and request.user != oauth_user.user:
        # Logged in but the accounts do not match, prevent linking
        return redirect_with_message(
            request,
            "error",
            "This OAuth account is already linked to another user account.",
            "users:profile",
        )
    else:
        # Login and update the OAuthUser with the latest info
        UserAuthManager.create_or_update_oauth_user(
            oauth_user.user, user_info)
        auth_login(request, oauth_user.user)

        if next_url:
            return redirect(next_url)

        return redirect("core:index")


def handle_oauth_user_not_found(request, user_info, next_url, UserAuthManager):
    if request.user.is_authenticated:
        # User is logged in, link the account if not linked to another OAuth account
        UserAuthManager.create_or_update_oauth_user(
            request.user, user_info)
        return redirect_with_message(
            request,
            "success",
            "Your account has been linked successfully.",
            "users:profile",
        )
    else:
        # No OAuthUser found, attempt to find or create a new user
        try:
            user = UserAuthManager.get_user_by_email(user_info.get("email"))
            # Existing user found, ask to link accounts manually
            return redirect_with_message(
                request,
                "error",
                "An account with your email already exists. Please log in and link your accounts manually.",
                "users:login",
            )
        except User.DoesNotExist:
            # No User found, save the OAuth user info in the session for further processing in the signup flow
            request.session["oauth_user_info"] = user_info

            if next_url:
                request.session["next_url_after_oauth_signup"] = next_url

            # Redirect to a special OAuth signup page to complete their profile
            return redirect("oauth:signup_username")


def authenticate_oauth(request, provider_name, user_info, next_url):
    email = user_info.get("email")
    if not email:
        logger.error("OAuth callback did not return an email")
        return redirect_with_message(
            request,
            "error",
            "We were unable to retrieve your email address. Please provide it manually.",
            "users:login",
        )
    try:
        # otherwise circular import error
        from users.utils import UserAuthManager
        # Check if the email is associated with an existing OAuthUser
        oauth_user = UserAuthManager.get_oauth_user(email, provider_name)
        logger.info(
            f"OAuthUser found: {oauth_user.user.username if oauth_user else None}")

        if oauth_user:
            return handle_oauth_user_found(request, oauth_user, user_info, next_url, UserAuthManager)
        else:
            return handle_oauth_user_not_found(request, user_info, next_url, UserAuthManager)
    except User.DoesNotExist:
        request.session["oauth_user_info"] = user_info
        if next_url:
            request.session["next_url_after_oauth_signup"] = next_url
        return redirect("oauth:signup_username")
    except Exception as e:
        logger.error(f"Error during oauth user authentication process: {e}")
        return redirect_with_message(request, 'error', "There was an error processing your request. Please try again.", "users:login")
